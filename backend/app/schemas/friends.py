"""好友与私信 Schema"""
from datetime import datetime
from pydantic import BaseModel, Field


class UserBrief(BaseModel):
    id: int
    username: str
    nickname: str | None = None

    class Config:
        from_attributes = True


class FriendRequestCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class FriendshipItem(BaseModel):
    id: int
    user: UserBrief
    status: str
    is_incoming: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FriendListResponse(BaseModel):
    friends: list[FriendshipItem]
    pending: list[FriendshipItem]


class FriendMessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class FriendMessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    is_mine: bool

    class Config:
        from_attributes = True


class FriendMessageListResponse(BaseModel):
    items: list[FriendMessageResponse]


class UnreadSummaryItem(BaseModel):
    friend_id: int
    friend: UserBrief
    unread_count: int
    last_content: str
    last_message_id: int
    last_at: datetime


class UnreadSummaryResponse(BaseModel):
    total: int
    items: list[UnreadSummaryItem]
