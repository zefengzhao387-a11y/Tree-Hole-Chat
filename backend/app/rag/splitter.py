"""
Text Splitter 模块
使用递归字符分割器对日记文本进行分块
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from app.config import settings


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """获取文本分割器实例"""
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
        keep_separator=True,
    )


def split_documents(documents: List[Document]) -> List[Document]:
    """
    对文档列表进行分割
    """
    splitter = get_text_splitter()
    return splitter.split_documents(documents)
