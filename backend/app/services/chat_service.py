"""
树洞对话业务逻辑
"""
import json
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, delete
from app.models.conversation import Conversation
from app.rag.chain import get_llm, retrieve_context
from app.rag.prompts import TREEHOLE_CHAT_PROMPT
from app.config import settings


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


async def chat_stream(
    db: AsyncSession,
    user_id: int,
    user_message: str,
) -> AsyncGenerator[str, None]:
    await save_message(db, user_id, "user", user_message)

    context, diary_ids = retrieve_context(user_message, user_id=user_id)

    history_msgs = await get_chat_history(db, user_id)
    history_str = format_history(history_msgs)

    llm = get_llm(temperature=0.7, streaming=True)
    full_response = ""

    try:
        messages_for_llm = TREEHOLE_CHAT_PROMPT.format_messages(
            context=context,
            history=history_str,
            query=user_message,
        )

        async for chunk in llm.astream(messages_for_llm):
            if chunk.content:
                full_response += chunk.content
                yield f"data: {json.dumps({'content': chunk.content, 'done': False}, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'content': '', 'done': True, 'diary_ids': diary_ids}, ensure_ascii=False)}\n\n"
        await save_message(db, user_id, "assistant", full_response, diary_ids)

    except Exception as e:
        error_msg = "\n\n(抱歉，我现在有点走神了...可以再说一次吗？)"
        yield f"data: {json.dumps({'content': error_msg, 'done': True, 'error': str(e)}, ensure_ascii=False)}\n\n"
