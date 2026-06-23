"""
Embedding 模块封装
优先使用本地 HuggingFace Embedding（无需API费用），可选 DeepSeek Embedding API
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

_embeddings = None


def get_embeddings():
    """获取 Embedding 模型实例（单例，避免重复加载占满内存）"""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings
