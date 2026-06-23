"""
数据库初始化与 Session 管理
使用 SQLAlchemy 异步引擎 + SQLite
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# 将 DATABASE_URL 开头的 sqlite+aiosqlite 替换为 sqlite+aiosqlite（保持一致）
database_url = settings.DATABASE_URL
if "sqlite" in database_url and "aiosqlite" not in database_url:
    database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """FastAPI 依赖注入：获取数据库 session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """初始化数据库表，并尝试补充新增字段"""
    import app.models  # noqa: F401 — 注册 User 等全部 ORM 表

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_migrate_columns)


def _migrate_columns(connection):
    """SQLite 简易迁移：为旧库补充 user_id 等字段"""
    from sqlalchemy import inspect, text

    inspector = inspect(connection)
    if "diaries" in inspector.get_table_names():
        cols = {c["name"] for c in inspector.get_columns("diaries")}
        if "user_id" not in cols:
            connection.execute(text("ALTER TABLE diaries ADD COLUMN user_id INTEGER"))
    if "conversations" in inspector.get_table_names():
        cols = {c["name"] for c in inspector.get_columns("conversations")}
        if "user_id" not in cols:
            connection.execute(text("ALTER TABLE conversations ADD COLUMN user_id INTEGER"))
