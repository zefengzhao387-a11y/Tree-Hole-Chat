"""
对话相关 Pydantic 模型
"""
from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """发送消息请求"""
    message: str = Field(..., min_length=1, description="用户消息")


class ChatMessage(BaseModel):
    """单条对话消息"""
    id: int
    role: str
    content: str
    diary_ids: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """对话历史响应"""
    messages: list[ChatMessage]
    total: int
