"""好友与私信 API"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.deps.auth import get_current_user
from app.schemas.friends import (
    UserBrief,
    FriendRequestCreate,
    FriendListResponse,
    FriendMessageCreate,
    FriendMessageListResponse,
    FriendMessageResponse,
    FriendshipItem,
    UnreadSummaryResponse,
)
from app.services import friend_service

router = APIRouter(prefix="/api/friends", tags=["好友"])


@router.get("/search", response_model=list[UserBrief])
async def search_users(
    q: str = Query(..., min_length=2, max_length=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.search_users(db, user.id, q)


@router.get("", response_model=FriendListResponse)
async def list_friends(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.list_friends(db, user.id)


@router.post("/request", response_model=FriendshipItem, status_code=201)
async def send_friend_request(
    data: FriendRequestCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.send_friend_request(db, user, data.username)


@router.post("/{friendship_id}/accept", response_model=FriendshipItem)
async def accept_friend_request(
    friendship_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.respond_friend_request(db, user, friendship_id, accept=True)


@router.post("/{friendship_id}/reject", response_model=FriendshipItem)
async def reject_friend_request(
    friendship_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.respond_friend_request(db, user, friendship_id, accept=False)


@router.delete("/{friendship_id}", status_code=204)
async def remove_friend(
    friendship_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await friend_service.remove_friend(db, user.id, friendship_id)


@router.get("/unread/summary", response_model=UnreadSummaryResponse)
async def unread_summary(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.get_unread_summary(db, user.id)


@router.get("/{friend_id}/messages", response_model=FriendMessageListResponse)
async def get_messages(
    friend_id: int,
    after_id: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items = await friend_service.list_messages(db, user.id, friend_id, after_id, limit)
    return FriendMessageListResponse(items=items)


@router.post("/{friend_id}/messages", response_model=FriendMessageResponse, status_code=201)
async def send_message(
    friend_id: int,
    data: FriendMessageCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await friend_service.send_message(db, user.id, friend_id, data.content)
