"""
Embedding 模块封装
优先使用本地 HuggingFace Embedding（无需API费用），可选 DeepSeek Embedding API
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings


def get_embeddings():
    """
    获取 Embedding 模型实例
    使用 BGE 中文小模型，本地运行，免费且效果好
    """
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
