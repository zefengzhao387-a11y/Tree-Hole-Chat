"""
情感分析相关 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel


class EmotionAnalysisResponse(BaseModel):
    """情感分析结果响应"""
    id: int
    diary_id: int
    primary_emotion: str | None = None
    emotion_scores: str | None = None  # JSON字符串
    sentiment: str | None = None
    intensity: int | None = None
    keywords: str | None = None
    summary: str | None = None
    suggestion: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class EmotionPoint(BaseModel):
    """单个时间点的情感数据"""
    date: str
    diary_id: int
    diary_title: str
    primary_emotion: str | None = None
    sentiment: str | None = None
    intensity: int | None = None


class TrendResponse(BaseModel):
    """情感趋势响应"""
    points: list[EmotionPoint]


class ReportResponse(BaseModel):
    """情感报告响应"""
    start_date: str
    end_date: str
    total_diaries: int
    dominant_emotion: str | None = None
    sentiment_distribution: dict  # {"positive": 5, "negative": 3, "neutral": 2}
    average_intensity: float
    trend_summary: str  # LLM生成的趋势总结
    suggestions: list[str]
