"""
日记数据模型
"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="日记标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="日记正文")
    mood_label: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="用户自选心情标签")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联：一篇日记有一条情感分析结果
    emotion_analysis: Mapped["EmotionAnalysis | None"] = relationship(
        "EmotionAnalysis", back_populates="diary", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Diary(id={self.id}, title='{self.title[:20]}...')>"
