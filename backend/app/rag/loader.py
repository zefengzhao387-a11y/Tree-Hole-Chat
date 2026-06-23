"""
Document Loader 模块
将日记文本加载为 LangChain Document 对象
"""
from langchain_core.documents import Document
from datetime import datetime
from typing import List


def load_diary_documents(
    diary_id: int,
    title: str,
    content: str,
    date: datetime,
    primary_emotion: str | None = None,
    user_id: int | None = None,
) -> List[Document]:
    metadata = {
        "diary_id": diary_id,
        "user_id": user_id,
        "title": title,
        "date": date.isoformat() if isinstance(date, datetime) else str(date),
        "primary_emotion": primary_emotion or "未知",
    }

    doc = Document(page_content=content, metadata=metadata)
    return [doc]


def load_multiple_diaries(diaries: list) -> List[Document]:
    """
    批量加载多篇日记为 Document 列表
    diaries: [{"id": 1, "title": "...", "content": "...", "created_at": ..., "primary_emotion": "..."}, ...]
    """
    documents = []
    for diary in diaries:
        metadata = {
            "diary_id": diary["id"],
            "title": diary["title"],
            "date": diary["created_at"].isoformat() if isinstance(diary.get("created_at"), datetime) else str(diary.get("created_at", "")),
            "primary_emotion": diary.get("primary_emotion") or "未知",
        }
        documents.append(Document(page_content=diary["content"], metadata=metadata))
    return documents
