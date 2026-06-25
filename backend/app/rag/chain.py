"""
RAG Chain 组装模块
将检索、Prompt组装、LLM生成串联为完整流程
"""
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from app.config import settings
from app.rag.retriever import hybrid_search, llm_rerank
from app.rag.prompts import TREEHOLE_CHAT_PROMPT, QUERY_REWRITE_PROMPT, EMOTION_ANALYSIS_PROMPT
import json
import re


def get_llm(temperature: float = 0.7, streaming: bool = False) -> ChatOpenAI:
    """
    获取 DeepSeek LLM 实例
    兼容 OpenAI API 格式
    """
    return ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        temperature=temperature,
        streaming=streaming,
        timeout=120,
        max_retries=1,
    )


def build_rag_chain():
    """
    构建完整的 RAG Chain（非流式）
    用于非流式场景，返回完整结果
    """
    llm = get_llm(temperature=0.7, streaming=False)
    chain = TREEHOLE_CHAT_PROMPT | llm | StrOutputParser()
    return chain


def rewrite_query(query: str) -> str:
    """
    Query Rewrite：将用户自然语言改写为检索关键词
    """
    if not settings.DEEPSEEK_API_KEY or settings.DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        # 没有配置API Key时，直接返回原查询
        return query

    llm = get_llm(temperature=0.3, streaming=False)
    prompt = QUERY_REWRITE_PROMPT.format(query=query)
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        rewritten = response.content.strip()
        # 合并原查询和改写后的关键词
        return f"{query} {rewritten}"
    except Exception:
        return query


def retrieve_context(query: str, user_id: int | None = None) -> tuple[str, list[int]]:
    """
    执行完整检索流程：Query Rewrite → Hybrid Search → Re-ranking
    """
    rewritten_query = rewrite_query(query)
    docs = hybrid_search(rewritten_query, user_id=user_id)
    return _build_context_from_docs(docs, allow_rerank=True, query=query)


def retrieve_context_light(
    query: str,
    user_id: int | None = None,
    allowed_diary_ids: set[int] | None = None,
) -> tuple[str, list[int]]:
    """
    轻量检索：仅混合检索，不额外调用 LLM（对话场景更稳、更快）
    """
    docs = hybrid_search(query, user_id=user_id, allowed_diary_ids=allowed_diary_ids)
    return _build_context_from_docs(docs)


def _build_context_from_docs(docs, *, allow_rerank: bool = False, query: str = "") -> tuple[str, list[int]]:
    if not docs:
        return "暂无相关日记", []

    if allow_rerank and len(docs) > settings.RERANK_TOP_K and settings.DEEPSEEK_API_KEY not in ("", "your_deepseek_api_key_here"):
        try:
            llm = get_llm(temperature=0.3, streaming=False)
            docs = llm_rerank(query, docs, llm)
        except Exception:
            docs = docs[:settings.RERANK_TOP_K]

    context_parts = []
    diary_ids = []
    seen_diary_ids = set()
    for i, doc in enumerate(docs):
        diary_id = doc.metadata.get("diary_id")
        if diary_id is not None:
            try:
                diary_id = int(diary_id)
            except (TypeError, ValueError):
                pass
            if diary_id not in seen_diary_ids:
                seen_diary_ids.add(diary_id)
                diary_ids.append(diary_id)
        title = doc.metadata.get("title", "无标题")
        date = doc.metadata.get("date", "未知日期")
        emotion = doc.metadata.get("primary_emotion", "未知")
        snippet = doc.page_content[:300].replace("\n", " ")
        context_parts.append(
            f"[日记{i+1}] 标题:《{title}》| 日期:{date} | 情绪:{emotion}\n内容:{snippet}"
        )

    context = "\n\n---\n\n".join(context_parts)
    return context, diary_ids


def analyze_emotion(diary_content: str) -> dict:
    """
    使用 LLM 对日记内容进行情感分析
    返回结构化分析结果
    """
    try:
        llm = get_llm(temperature=0.3, streaming=False)
        prompt = EMOTION_ANALYSIS_PROMPT.format(diary_content=diary_content)

        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()

        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            return json.loads(json_match.group())
        return _get_default_analysis()

    except Exception as e:
        print(f"情感分析失败: {e}")
        return _get_default_analysis()


def _get_default_analysis() -> dict:
    """默认情感分析结果（LLM调用失败时的后备）"""
    return {
        "primary_emotion": "未知",
        "emotion_scores": {
            "joy": 0.5, "sadness": 0.5, "anxiety": 0.5,
            "anger": 0.5, "calm": 0.5, "fear": 0.5,
            "loneliness": 0.5, "gratitude": 0.5
        },
        "sentiment": "neutral",
        "intensity": 5,
        "keywords": ["日记"],
        "summary": "这是一篇日记记录",
        "suggestion": "继续保持记录日记的好习惯哦~"
    }
