"""
情感分析 API 路由
"""
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.deps.auth import get_current_user
from app.schemas.analysis import EmotionAnalysisResponse, TrendResponse, EmotionPoint, ReportResponse
from app.services import diary_service, emotion_analyzer
from app.rag.chain import get_llm, analyze_emotion
from app.models.diary import Diary
from app.config import settings
from langchain_core.messages import HumanMessage

router = APIRouter(prefix="/api/analysis", tags=["情感分析"])


@router.post("/{diary_id}", response_model=EmotionAnalysisResponse)
async def run_analysis(
    diary_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """对指定日记执行/重新执行情感分析"""
    diary = await diary_service.get_diary_by_id(db, diary_id, user.id)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    analysis = await emotion_analyzer.analyze_diary_emotion(db, diary)
    return EmotionAnalysisResponse(
        id=analysis.id,
        diary_id=analysis.diary_id,
        primary_emotion=analysis.primary_emotion,
        emotion_scores=analysis.emotion_scores,
        sentiment=analysis.sentiment,
        intensity=analysis.intensity,
        keywords=analysis.keywords,
        summary=analysis.summary,
        suggestion=analysis.suggestion,
        created_at=analysis.created_at,
    )


@router.get("/trend", response_model=TrendResponse)
async def get_emotion_trend(
    start_date: str | None = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: str | None = Query(None, description="结束日期 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """获取情感趋势数据"""
    # 默认最近30天
    from datetime import datetime, timedelta
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    diaries = await diary_service.get_diaries_in_range(db, user.id, start_date, end_date)

    points = []
    for d in diaries:
        if d.emotion_analysis:
            points.append(EmotionPoint(
                date=d.created_at.strftime("%Y-%m-%d %H:%M"),
                diary_id=d.id,
                diary_title=d.title,
                primary_emotion=d.emotion_analysis.primary_emotion,
                sentiment=d.emotion_analysis.sentiment,
                intensity=d.emotion_analysis.intensity,
            ))

    return TrendResponse(points=points)


@router.get("/report", response_model=ReportResponse)
async def get_emotion_report(
    start_date: str | None = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: str | None = Query(None, description="结束日期 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """获取时间段情感分析报告"""
    from datetime import datetime, timedelta
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    diaries = await diary_service.get_diaries_in_range(db, user.id, start_date, end_date)

    if not diaries:
        return ReportResponse(
            start_date=start_date,
            end_date=end_date,
            total_diaries=0,
            sentiment_distribution={"positive": 0, "negative": 0, "neutral": 0},
            average_intensity=0,
            trend_summary="该时间段暂无日记记录",
            suggestions=["开始写日记吧，记录心情是了解自己的第一步~"],
        )

    # 统计
    pos = neg = neu = 0
    emotions_count = {}
    total_intensity = 0
    count_with_analysis = 0

    for d in diaries:
        if d.emotion_analysis:
            count_with_analysis += 1
            s = d.emotion_analysis.sentiment
            if s == "positive":
                pos += 1
            elif s == "negative":
                neg += 1
            else:
                neu += 1

            em = d.emotion_analysis.primary_emotion
            if em:
                emotions_count[em] = emotions_count.get(em, 0) + 1

            if d.emotion_analysis.intensity:
                total_intensity += d.emotion_analysis.intensity

    avg_intensity = total_intensity / count_with_analysis if count_with_analysis > 0 else 0
    dominant_emotion = max(emotions_count, key=emotions_count.get) if emotions_count else None

    # 生成趋势总结（LLM）
    trend_summary = ""
    suggestions = []
    try:
        if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY not in ("", "your_deepseek_api_key_here"):
            emotion_flow = " → ".join(
                [f"{d.emotion_analysis.primary_emotion}" for d in diaries if d.emotion_analysis][-10:]
            )
            human_msg = f"""以下是用户在 {start_date} 到 {end_date} 期间记录了 {len(diaries)} 篇日记的情感数据：

情感分布：积极 {pos} 篇，消极 {neg} 篇，中性 {neu} 篇
主要情绪变化：{emotion_flow}
平均情绪强度：{avg_intensity:.1f}/10

请用温暖的口吻写一段情感趋势总结（80-150字），并给出2-3条小建议。总结和建议分别用【总结】和【建议】开头。"""

            llm = get_llm(temperature=0.5, streaming=False)
            response = llm.invoke([HumanMessage(content=human_msg)])
            content = response.content

            if "【总结】" in content:
                parts = content.split("【建议】")
                trend_summary = parts[0].replace("【总结】", "").strip()
                if len(parts) > 1:
                    suggestions = [s.strip().lstrip("0123456789.、 ") for s in parts[1].split("\n") if s.strip()]
    except Exception:
        pass

    if not trend_summary:
        trend_summary = f"在{start_date}至{end_date}期间，你共记录了{len(diaries)}篇日记，整体情绪以{dominant_emotion or '多样'}为主。"
    if not suggestions:
        suggestions = ["继续保持记录日记的习惯~", "尝试每天写下三件感恩的小事"]

    return ReportResponse(
        start_date=start_date,
        end_date=end_date,
        total_diaries=len(diaries),
        dominant_emotion=dominant_emotion,
        sentiment_distribution={"positive": pos, "negative": neg, "neutral": neu},
        average_intensity=round(avg_intensity, 1),
        trend_summary=trend_summary,
        suggestions=suggestions,
    )
