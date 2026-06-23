"""
情感分析结果数据模型
"""
from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class EmotionAnalysis(Base):
    __tablename__ = "emotion_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    diary_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("diaries.id", ondelete="CASCADE"), nullable=False, unique=True, comment="关联日记ID"
    )
    primary_emotion: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="主要情绪")
    emotion_scores: Mapped[str | None] = mapped_column(Text, nullable=True, comment="各情绪维度得分JSON")
    sentiment: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="积极/消极/中性")
    intensity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="情绪强度1-10")
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True, comment="情绪关键词JSON数组")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True, comment="LLM情感摘要")
    suggestion: Mapped[str | None] = mapped_column(Text, nullable=True, comment="LLM建议")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="分析时间")

    # 反向关联
    diary: Mapped["Diary"] = relationship("Diary", back_populates="emotion_analysis")

    def __repr__(self):
        return f"<EmotionAnalysis(diary_id={self.diary_id}, primary='{self.primary_emotion}')>"
