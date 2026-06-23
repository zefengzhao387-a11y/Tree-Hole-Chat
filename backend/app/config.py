"""
应用配置管理
使用 pydantic-settings 加载环境变量
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _parse_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "")
    if raw.strip():
        return [origin.strip() for origin in raw.split(",") if origin.strip()]
    return [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]


class Settings:
    """全局配置类"""

    # DeepSeek API
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # 数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/diary.db")
    DATABASE_URL_SYNC: str = DATABASE_URL.replace("+aiosqlite", "").replace("sqlite+aiosqlite", "sqlite")

    # Chroma 向量数据库
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
    CHROMA_COLLECTION_NAME: str = "diary_embeddings"

    # Embedding 模型
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-zh-v1.5"  # 本地轻量中文Embedding

    # 文本分割参数
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # 检索参数
    RETRIEVAL_TOP_K: int = 5
    HYBRID_SEARCH_TOP_K: int = 8
    RERANK_TOP_K: int = 3

    # 对话记忆
    CONVERSATION_MEMORY_K: int = 10

    # 应用
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))

    # CORS（生产：CORS_ORIGINS=https://tree-hole-chat.vercel.app）
    # Vercel 预览域名每次不同，可设 CORS_ORIGIN_REGEX=https://.*\.vercel\.app
    CORS_ORIGINS: list[str] = _parse_cors_origins()
    CORS_ORIGIN_REGEX: str = os.getenv("CORS_ORIGIN_REGEX", "")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "treehole-dev-secret-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "10080"))  # 7 天


settings = Settings()
