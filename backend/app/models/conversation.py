"""
对话记录数据模型
"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(10), nullable=False, comment="user/assistant")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="消息内容")
    diary_ids: Mapped[str | None] = mapped_column(Text, nullable=True, comment="引用的日记ID JSON数组")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="消息时间")

    def __repr__(self):
        return f"<Conversation(role='{self.role}', content='{self.content[:30]}...')>"
