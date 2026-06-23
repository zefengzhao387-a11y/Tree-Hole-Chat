"""
高级检索模块
实现 Hybrid Search（向量检索 + BM25关键词检索）和 Re-ranking
"""
from typing import List
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import jieba
from app.rag.vector_store import similarity_search
from app.config import settings


def _tokenize(text: str) -> List[str]:
    """中文分词"""
    return list(jieba.cut(text))


def bm25_search(query: str, documents: List[Document], top_k: int = 3) -> List[Document]:
    """
    BM25 关键词检索
    对所有文档内容进行中文分词后建立 BM25 索引，然后检索
    """
    if not documents:
        return []

    # 分词
    tokenized_docs = [_tokenize(doc.page_content) for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)

    tokenized_query = _tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    # 取 Top-K
    doc_score_pairs = list(zip(documents, scores))
    doc_score_pairs.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in doc_score_pairs[:top_k]]


def hybrid_search(
    query: str,
    user_id: int | None = None,
    allowed_diary_ids: set[int] | None = None,
) -> List[Document]:
    """
    混合检索：向量语义检索 + BM25 关键词检索
    """
    semantic_results = similarity_search(
        query, top_k=settings.RETRIEVAL_TOP_K, user_id=user_id, allowed_diary_ids=allowed_diary_ids
    )
    all_docs = similarity_search(
        query, top_k=settings.HYBRID_SEARCH_TOP_K, user_id=user_id, allowed_diary_ids=allowed_diary_ids
    )
    keyword_results = bm25_search(query, all_docs, top_k=3)

    # 3. 合并去重（按 diary_id）
    seen_ids = set()
    merged = []
    for doc in semantic_results + keyword_results:
        did = doc.metadata.get("diary_id")
        if did not in seen_ids:
            seen_ids.add(did)
            merged.append(doc)

    return merged[:settings.HYBRID_SEARCH_TOP_K]


def llm_rerank(query: str, documents: List[Document], llm) -> List[Document]:
    """
    使用 LLM 对检索结果进行重排序
    返回最相关的 Top-K 文档
    """
    if len(documents) <= settings.RERANK_TOP_K:
        return documents

    # 构建排序 prompt
    doc_texts = []
    for i, doc in enumerate(documents):
        snippet = doc.page_content[:200].replace("\n", " ")
        doc_texts.append(f"[{i}] 标题:{doc.metadata.get('title','')} | 内容:{snippet}")

    prompt = f"""用户当前话题："{query}"
以下是用户过去的一些日记片段，请根据与当前话题的情感相关性（最重要）、主题相似度进行排序。
只返回排序后的文档编号（用逗号分隔，如 "3,0,5,1,2,4"），不要其他内容。

{chr(10).join(doc_texts)}

排序结果（仅返回编号）："""

    try:
        from langchain_core.messages import HumanMessage
        response = llm.invoke([HumanMessage(content=prompt)])
        # 解析排序结果
        order_str = response.content.strip()
        # 提取数字
        import re
        indices = [int(x) for x in re.findall(r'\d+', order_str)]
        # 按顺序返回
        reranked = [documents[i] for i in indices if i < len(documents)]
        return reranked[:settings.RERANK_TOP_K]
    except Exception:
        # 排序失败则返回原列表的前N个
        return documents[:settings.RERANK_TOP_K]
