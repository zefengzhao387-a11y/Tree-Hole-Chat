"""
树洞对话业务逻辑
"""
import asyncio
import json
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, delete
from app.models.conversation import Conversation
from app.database import AsyncSessionLocal
from app.rag.chain import get_llm, retrieve_context_light
from app.rag.prompts import TREEHOLE_CHAT_PROMPT
from app.config import settings

logger = logging.getLogger(__name__)


async def get_chat_history(db: AsyncSession, user_id: int, limit: int = 50) -> list[Conversation]:
    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.created_at))
        .limit(limit)
    )
    result = await db.execute(query)
    messages = list(result.scalars().all())
    messages.reverse()
    return messages


async def save_message(
    db: AsyncSession,
    user_id: int,
    role: str,
    content: str,
    diary_ids: list[int] | None = None,
) -> Conversation:
    msg = Conversation(
        user_id=user_id,
        role=role,
        content=content,
        diary_ids=json.dumps(diary_ids, ensure_ascii=False) if diary_ids else None,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def clear_chat_history(db: AsyncSession, user_id: int):
    await db.execute(delete(Conversation).where(Conversation.user_id == user_id))
    await db.commit()


def format_history(messages: list[Conversation]) -> str:
    k = settings.CONVERSATION_MEMORY_K * 2
    recent = messages[-k:]
    if not recent:
        return "（这是对话的开始）"
    lines = []
    for msg in recent:
        role_label = "用户" if msg.role == "user" else "小树"
        lines.append(f"{role_label}: {msg.content}")
    return "\n".join(lines)


def _extract_chunk_content(content) -> str:
    if not content:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return str(content)


def _chunk_text(text: str, size: int = 24):
    for i in range(0, len(text), size):
        yield text[i:i + size]


def _sse_payload(content: str, *, done: bool = False, diary_ids=None, error: str | None = None) -> str:
    data = {"content": content, "done": done}
    if diary_ids is not None:
        data["diary_ids"] = diary_ids
    if error:
        data["error"] = error
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def _user_facing_llm_error(exc: Exception) -> str:
    msg = str(exc)
    if "402" in msg or "Insufficient Balance" in msg:
        return "\n\n(DeepSeek API 余额不足，请在 platform.deepseek.com 充值后重试。)"
    if "401" in msg or "Authentication" in msg or "invalid api key" in msg.lower():
        return "\n\n(DeepSeek API Key 无效，请检查 Railway 环境变量 DEEPSEEK_API_KEY。)"
    if "429" in msg or "rate limit" in msg.lower():
        return "\n\n(请求太频繁了，稍等几秒再试试吧。)"
    return "\n\n(抱歉，我现在有点走神了...可以再说一次吗？)"


def _is_non_retryable_llm_error(exc: Exception) -> bool:
    msg = str(exc)
    return any(token in msg for token in ("402", "401", "Insufficient Balance", "invalid api key"))


async def _stream_llm(messages_for_llm, llm) -> AsyncGenerator[str, None]:
    """流式生成；失败时降级为非流式"""
    got_content = False
    try:
        async for chunk in llm.astream(messages_for_llm):
            content = _extract_chunk_content(chunk.content)
            if content:
                got_content = True
                yield _sse_payload(content)
        if not got_content:
            raise RuntimeError("LLM stream returned empty response")
    except Exception as stream_err:
        if _is_non_retryable_llm_error(stream_err):
            raise stream_err
        logger.warning("chat stream failed, fallback to invoke: %s", stream_err)
        llm_sync = get_llm(temperature=0.7, streaming=False)
        response = await asyncio.to_thread(llm_sync.invoke, messages_for_llm)
        text = _extract_chunk_content(response.content).strip()
        if not text:
            raise stream_err
        for piece in _chunk_text(text):
            yield _sse_payload(piece)


async def _get_user_diary_ids(user_id: int) -> set[int]:
    from app.models.diary import Diary

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Diary.id).where(Diary.user_id == user_id))
        return set(result.scalars().all())


async def chat_stream(
    user_id: int,
    user_message: str,
) -> AsyncGenerator[str, None]:
    """流式对话：独立管理 DB session，避免 SSE 期间连接泄漏"""
    if not settings.DEEPSEEK_API_KEY or settings.DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        yield _sse_payload(
            "\n\n(后端未配置 DEEPSEEK_API_KEY，请联系管理员。)",
            done=True,
            error="missing_api_key",
        )
        return

    async with AsyncSessionLocal() as db:
        await save_message(db, user_id, "user", user_message)
        history_msgs = await get_chat_history(db, user_id)
        history_str = format_history(history_msgs)

    try:
        allowed_diary_ids = await _get_user_diary_ids(user_id)
        context, diary_ids = await asyncio.to_thread(
            retrieve_context_light,
            user_message,
            user_id,
            allowed_diary_ids,
        )
    except Exception as rag_err:
        logger.warning("RAG retrieve failed, continue without context: %s", rag_err)
        context, diary_ids = "暂无相关日记", []

    llm = get_llm(temperature=0.7, streaming=True)
    full_response = ""

    try:
        messages_for_llm = TREEHOLE_CHAT_PROMPT.format_messages(
            context=context,
            history=history_str,
            query=user_message,
        )

        async for event in _stream_llm(messages_for_llm, llm):
            yield event
            if event.startswith("data:"):
                try:
                    payload = json.loads(event[6:].strip())
                    if payload.get("content") and not payload.get("done"):
                        full_response += payload["content"]
                except json.JSONDecodeError:
                    pass

        yield _sse_payload("", done=True, diary_ids=diary_ids)

        try:
            async with AsyncSessionLocal() as db:
                await save_message(db, user_id, "assistant", full_response, diary_ids)
        except Exception as save_err:
            logger.exception("save assistant message failed: %s", save_err)

    except Exception as e:
        logger.exception("chat_stream failed: %s", e)
        error_text = _user_facing_llm_error(e).strip()
        yield _sse_payload(
            error_text,
            done=True,
            diary_ids=diary_ids,
            error=str(e),
        )
        try:
            async with AsyncSessionLocal() as db:
                await save_message(db, user_id, "assistant", error_text, diary_ids)
        except Exception as save_err:
            logger.exception("save error assistant message failed: %s", save_err)
