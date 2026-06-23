"""
Chroma 向量数据库管理模块
"""
import os
import shutil
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
from app.config import settings
from app.rag.embeddings import get_embeddings


# 全局单例
_vector_store: Chroma | None = None


def get_vector_store() -> Chroma:
    """获取 Chroma 向量存储实例（单例）"""
    global _vector_store
    if _vector_store is None:
        persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIRECTORY)
        os.makedirs(persist_dir, exist_ok=True)

        _vector_store = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=get_embeddings(),
            persist_directory=persist_dir,
        )
    return _vector_store


def add_documents(documents: List[Document]):
    """将文档向量化后存入 Chroma"""
    if not documents:
        return
    store = get_vector_store()
    store.add_documents(documents)


def update_diary_vectors(diary_id: int, documents: List[Document]):
    """
    更新指定日记的向量：先删除旧向量，再添加新向量
    """
    store = get_vector_store()
    # 删除该日记的旧向量
    try:
        results = store.get(where={"diary_id": diary_id})
        if results and results.get("ids"):
            store.delete(ids=results["ids"])
    except Exception:
        pass  # 如果没有旧数据则跳过
    # 添加新向量
    add_documents(documents)


def delete_diary_vectors(diary_id: int):
    """删除指定日记的所有向量"""
    store = get_vector_store()
    try:
        results = store.get(where={"diary_id": diary_id})
        if results and results.get("ids"):
            store.delete(ids=results["ids"])
    except Exception:
        pass


def _count_documents(store: Chroma, user_id: int | None = None) -> int:
    """统计可用向量条数，避免 k 大于索引大小"""
    try:
        if user_id is not None:
            for uid in (user_id, str(user_id)):
                results = store.get(where={"user_id": uid}, include=[])
                ids = results.get("ids") or []
                if ids:
                    return len(ids)
            return 0
        return store._collection.count()
    except Exception:
        return 0


def _doc_belongs_to_user(
    doc: Document,
    user_id: int,
    allowed_diary_ids: set[int] | None = None,
) -> bool:
    meta_uid = doc.metadata.get("user_id")
    if meta_uid is not None:
        return str(meta_uid) == str(user_id)

    diary_id = doc.metadata.get("diary_id")
    if diary_id is None or not allowed_diary_ids:
        return False
    try:
        return int(diary_id) in allowed_diary_ids
    except (TypeError, ValueError):
        return False


def _filter_docs_for_user(
    docs: List[Document],
    user_id: int,
    allowed_diary_ids: set[int] | None = None,
    limit: int | None = None,
) -> List[Document]:
    filtered = [
        doc for doc in docs
        if _doc_belongs_to_user(doc, user_id, allowed_diary_ids)
    ]
    return filtered[:limit] if limit else filtered


def similarity_search(
    query: str,
    top_k: int | None = None,
    user_id: int | None = None,
    allowed_diary_ids: set[int] | None = None,
) -> List[Document]:
    """向量相似度检索，可按用户过滤"""
    store = get_vector_store()
    k = top_k or settings.RETRIEVAL_TOP_K
    total = _count_documents(store, None)
    if total == 0:
        return []

    if user_id is not None:
        available = _count_documents(store, user_id)
        if available > 0:
            search_k = min(k, available)
            for uid in (user_id, str(user_id)):
                try:
                    return store.similarity_search(
                        query,
                        k=search_k,
                        filter={"user_id": uid},
                    )
                except Exception:
                    continue

        # 旧向量可能没有 user_id 字段：先全库检索，再按用户日记过滤
        search_k = min(max(k * 3, k), total)
        raw_docs = store.similarity_search(query, k=search_k)
        filtered = _filter_docs_for_user(raw_docs, user_id, allowed_diary_ids, limit=k)
        if filtered:
            return filtered

    available = total
    search_k = min(k, available)
    return store.similarity_search(query, k=search_k)


def reset_vector_store():
    """重置向量数据库（清空所有数据）"""
    global _vector_store
    persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIRECTORY)
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    _vector_store = None
    get_vector_store()
