"""
情感分析业务逻辑
"""
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.diary import Diary
from app.models.emotion_analysis import EmotionAnalysis
from app.rag.chain import analyze_emotion


async def ensure_diary_emotion(db: AsyncSession, diary: Diary) -> EmotionAnalysis | None:
    """确保日记有情感分析记录，缺失时补跑分析"""
    if diary.emotion_analysis:
        return diary.emotion_analysis
    try:
        analysis = await analyze_diary_emotion(db, diary)
        await db.refresh(diary, attribute_names=["emotion_analysis"])
        return analysis
    except Exception:
        return diary.emotion_analysis


async def analyze_diary_emotion(db: AsyncSession, diary: Diary) -> EmotionAnalysis:
    # 调用 LLM 进行情感分析
    result = analyze_emotion(diary.content)

    # 检查是否已有分析结果
    existing = await db.execute(
        select(EmotionAnalysis).where(EmotionAnalysis.diary_id == diary.id)
    )
    analysis = existing.scalar_one_or_none()

    if analysis:
        # 更新已有记录
        analysis.primary_emotion = result.get("primary_emotion")
        analysis.emotion_scores = json.dumps(result.get("emotion_scores", {}), ensure_ascii=False)
        analysis.sentiment = result.get("sentiment")
        analysis.intensity = result.get("intensity", 5)
        analysis.keywords = json.dumps(result.get("keywords", []), ensure_ascii=False)
        analysis.summary = result.get("summary")
        analysis.suggestion = result.get("suggestion")
    else:
        # 创建新记录
        analysis = EmotionAnalysis(
            diary_id=diary.id,
            primary_emotion=result.get("primary_emotion"),
            emotion_scores=json.dumps(result.get("emotion_scores", {}), ensure_ascii=False),
            sentiment=result.get("sentiment"),
            intensity=result.get("intensity", 5),
            keywords=json.dumps(result.get("keywords", []), ensure_ascii=False),
            summary=result.get("summary"),
            suggestion=result.get("suggestion"),
        )
        db.add(analysis)

    await db.commit()
    # 不调用 refresh，避免异步会话懒加载问题（expire_on_commit=False 已保证对象有效）
    return analysis
