"""
FastAPI 应用入口
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_db, get_db
from app.models.user import User
from app.deps.auth import get_current_user
from app.routers import diary, analysis, chat, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化数据库"""
    await init_db()
    try:
        from app.rag.embeddings import get_embeddings
        await asyncio.to_thread(get_embeddings)
        logger = logging.getLogger(__name__)
        logger.info("Embedding model warmed up")
    except Exception as e:
        logging.getLogger(__name__).warning("Embedding warmup skipped: %s", e)
    yield


app = FastAPI(
    title="个人日记情感分析与解忧树洞对话系统",
    description="基于 LangChain 的个人日记情感分析与树洞对话系统 API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(diary.router)
app.include_router(analysis.router)
app.include_router(chat.router)


@app.get("/api/system/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "service": "日记情感分析与解忧树洞对话系统",
        "version": "1.0.0",
    }


@app.get("/api/system/stats")
async def system_stats(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """当前用户的系统统计"""
    from sqlalchemy import select, func
    from app.models.diary import Diary
    from app.models.emotion_analysis import EmotionAnalysis
    from app.models.conversation import Conversation

    diary_count = (await db.execute(
        select(func.count(Diary.id)).where(Diary.user_id == user.id)
    )).scalar() or 0

    analysis_count = (await db.execute(
        select(func.count(EmotionAnalysis.id))
        .join(Diary, Diary.id == EmotionAnalysis.diary_id)
        .where(Diary.user_id == user.id)
    )).scalar() or 0

    conv_count = (await db.execute(
        select(func.count(Conversation.id)).where(Conversation.user_id == user.id)
    )).scalar() or 0

    return {
        "diary_count": diary_count,
        "analysis_count": analysis_count,
        "conversation_count": conv_count,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
