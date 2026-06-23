"""
树洞对话 API 路由
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.deps.auth import get_current_user
from app.schemas.chat import ChatRequest, ChatHistoryResponse, ChatMessage
from app.services import chat_service

router = APIRouter(prefix="/api/chat", tags=["树洞对话"])


@router.post("/send")
async def send_message(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return StreamingResponse(
        chat_service.chat_stream(db, user.id, data.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    messages = await chat_service.get_chat_history(db, user.id)
    return ChatHistoryResponse(
        messages=[
            ChatMessage(
                id=m.id,
                role=m.role,
                content=m.content,
                diary_ids=m.diary_ids,
                created_at=m.created_at,
            )
            for m in messages
        ],
        total=len(messages),
    )


@router.delete("/history")
async def clear_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await chat_service.clear_chat_history(db, user.id)
    return {"message": "对话历史已清空"}
