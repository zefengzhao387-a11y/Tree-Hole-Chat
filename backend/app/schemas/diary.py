"""
日记相关 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


class DiaryCreate(BaseModel):
    """创建日记请求"""
    title: str = Field(..., min_length=1, max_length=200, description="日记标题")
    content: str = Field(..., min_length=1, description="日记正文")
    mood_label: str | None = Field(None, max_length=20, description="用户自选心情标签")


class DiaryUpdate(BaseModel):
    """更新日记请求"""
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
    mood_label: str | None = Field(None, max_length=20)


class EmotionAnalysisBrief(BaseModel):
    """情感分析简述（嵌套在日记响应中）"""
    id: int | None = None
    primary_emotion: str | None = None
    sentiment: str | None = None
    intensity: int | None = None
    summary: str | None = None

    class Config:
        from_attributes = True


class DiaryResponse(BaseModel):
    """日记响应"""
    id: int
    title: str
    content: str
    mood_label: str | None = None
    created_at: datetime
    updated_at: datetime
    emotion_analysis: EmotionAnalysisBrief | None = None

    class Config:
        from_attributes = True


class DiaryListResponse(BaseModel):
    """日记列表响应"""
    total: int
    items: list[DiaryResponse]
