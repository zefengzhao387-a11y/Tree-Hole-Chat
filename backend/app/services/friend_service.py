"""好友与私信业务逻辑"""
from datetime import datetime, timezone
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.user import User
from app.models.friendship import Friendship
from app.models.friend_message import FriendMessage
from app.schemas.friends import (
    UserBrief,
    FriendshipItem,
    FriendListResponse,
    FriendMessageResponse,
    UnreadSummaryResponse,
    UnreadSummaryItem,
)



async def search_users(db: AsyncSession, user_id: int, q: str, limit: int = 10) -> list[UserBrief]:
    keyword = q.strip()
    if len(keyword) < 2:
        return []
    result = await db.execute(
        select(User)
        .where(User.id != user_id, User.username.ilike(f"%{keyword}%"))
        .limit(limit)
    )
    return [UserBrief.model_validate(u) for u in result.scalars().all()]


async def _get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def _existing_friendship(db: AsyncSession, a: int, b: int) -> Friendship | None:
    result = await db.execute(
        select(Friendship).where(
            or_(
                and_(Friendship.requester_id == a, Friendship.addressee_id == b),
                and_(Friendship.requester_id == b, Friendship.addressee_id == a),
            )
        )
    )
    return result.scalar_one_or_none()


async def send_friend_request(db: AsyncSession, user: User, username: str) -> FriendshipItem:
    target = await _get_user_by_username(db, username.strip())
    if not target:
        raise HTTPException(status_code=404, detail="用户不存在")
    if target.id == user.id:
        raise HTTPException(status_code=400, detail="不能添加自己为好友")

    existing = await _existing_friendship(db, user.id, target.id)
    if existing:
        if existing.status == "accepted":
            raise HTTPException(status_code=400, detail="你们已经是好友了")
        if existing.status == "pending":
            if existing.requester_id == user.id:
                raise HTTPException(status_code=400, detail="好友请求已发送，请等待对方确认")
            existing.status = "accepted"
            existing.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            await db.commit()
            await db.refresh(existing)
            return _to_friendship_item(existing, user.id, target)
        raise HTTPException(status_code=400, detail="无法发送好友请求")

    row = Friendship(requester_id=user.id, addressee_id=target.id, status="pending")
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return _to_friendship_item(row, user.id, target)


def _other_user(friendship: Friendship, user_id: int) -> int:
    return friendship.addressee_id if friendship.requester_id == user_id else friendship.requester_id


async def _load_users_map(db: AsyncSession, user_ids: set[int]) -> dict[int, User]:
    if not user_ids:
        return {}
    result = await db.execute(select(User).where(User.id.in_(user_ids)))
    return {u.id: u for u in result.scalars().all()}


def _to_friendship_item(friendship: Friendship, user_id: int, other: User) -> FriendshipItem:
    return FriendshipItem(
        id=friendship.id,
        user=UserBrief.model_validate(other),
        status=friendship.status,
        is_incoming=friendship.addressee_id == user_id and friendship.status == "pending",
        created_at=friendship.created_at,
    )


async def list_friends(db: AsyncSession, user_id: int) -> FriendListResponse:
    result = await db.execute(
        select(Friendship).where(
            or_(Friendship.requester_id == user_id, Friendship.addressee_id == user_id),
            Friendship.status.in_(["accepted", "pending"]),
        ).order_by(Friendship.updated_at.desc())
    )
    rows = result.scalars().all()
    other_ids = {_other_user(r, user_id) for r in rows}
    users = await _load_users_map(db, other_ids)

    friends: list[FriendshipItem] = []
    pending: list[FriendshipItem] = []
    for row in rows:
        other = users.get(_other_user(row, user_id))
        if not other:
            continue
        item = _to_friendship_item(row, user_id, other)
        if row.status == "accepted":
            friends.append(item)
        else:
            pending.append(item)

    return FriendListResponse(friends=friends, pending=pending)


async def respond_friend_request(
    db: AsyncSession, user: User, friendship_id: int, accept: bool
) -> FriendshipItem:
    result = await db.execute(select(Friendship).where(Friendship.id == friendship_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="好友请求不存在")
    if row.addressee_id != user.id or row.status != "pending":
        raise HTTPException(status_code=403, detail="无权处理该请求")

    row.status = "accepted" if accept else "rejected"
    row.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    await db.commit()
    await db.refresh(row)

    other_id = row.requester_id
    other = (await db.execute(select(User).where(User.id == other_id))).scalar_one()
    return _to_friendship_item(row, user.id, other)


async def remove_friend(db: AsyncSession, user_id: int, friendship_id: int) -> None:
    result = await db.execute(select(Friendship).where(Friendship.id == friendship_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="好友关系不存在")
    if user_id not in (row.requester_id, row.addressee_id):
        raise HTTPException(status_code=403, detail="无权操作")
    if row.status != "accepted":
        raise HTTPException(status_code=400, detail="只能删除已接受的好友")
    await db.delete(row)
    await db.commit()


async def _ensure_friends(db: AsyncSession, user_id: int, friend_id: int) -> None:
    row = await _existing_friendship(db, user_id, friend_id)
    if not row or row.status != "accepted":
        raise HTTPException(status_code=403, detail="你们还不是好友，无法聊天")


async def list_messages(
    db: AsyncSession, user_id: int, friend_id: int, after_id: int = 0, limit: int = 50
) -> list[FriendMessageResponse]:
    await _ensure_friends(db, user_id, friend_id)
    result = await db.execute(
        select(FriendMessage)
        .where(
            or_(
                and_(FriendMessage.sender_id == user_id, FriendMessage.receiver_id == friend_id),
                and_(FriendMessage.sender_id == friend_id, FriendMessage.receiver_id == user_id),
            ),
            FriendMessage.id > after_id,
        )
        .order_by(FriendMessage.id.asc())
        .limit(limit)
    )
    items = result.scalars().all()

    unread_ids = [m.id for m in items if m.receiver_id == user_id and m.read_at is None]
    if unread_ids:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        for m in items:
            if m.id in unread_ids:
                m.read_at = now
        await db.commit()

    return [
        FriendMessageResponse(
            id=m.id,
            sender_id=m.sender_id,
            receiver_id=m.receiver_id,
            content=m.content,
            created_at=m.created_at,
            is_mine=m.sender_id == user_id,
        )
        for m in items
    ]


async def send_message(
    db: AsyncSession, user_id: int, friend_id: int, content: str
) -> FriendMessageResponse:
    await _ensure_friends(db, user_id, friend_id)
    msg = FriendMessage(sender_id=user_id, receiver_id=friend_id, content=content.strip())
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return FriendMessageResponse(
        id=msg.id,
        sender_id=msg.sender_id,
        receiver_id=msg.receiver_id,
        content=msg.content,
        created_at=msg.created_at,
        is_mine=True,
    )


async def get_unread_summary(db: AsyncSession, user_id: int) -> UnreadSummaryResponse:
    result = await db.execute(
        select(FriendMessage)
        .where(
            FriendMessage.receiver_id == user_id,
            FriendMessage.read_at.is_(None),
        )
        .order_by(FriendMessage.id.desc())
    )
    messages = result.scalars().all()

    grouped: dict[int, dict] = {}
    for msg in messages:
        if msg.sender_id not in grouped:
            grouped[msg.sender_id] = {"count": 0, "last": msg}
        grouped[msg.sender_id]["count"] += 1

    users = await _load_users_map(db, set(grouped.keys()))
    items: list[UnreadSummaryItem] = []
    for sender_id, info in grouped.items():
        sender = users.get(sender_id)
        if not sender:
            continue
        last = info["last"]
        items.append(
            UnreadSummaryItem(
                friend_id=sender_id,
                friend=UserBrief.model_validate(sender),
                unread_count=info["count"],
                last_content=last.content,
                last_message_id=last.id,
                last_at=last.created_at,
            )
        )

    items.sort(key=lambda x: x.last_at, reverse=True)
    total = sum(i.unread_count for i in items)
    return UnreadSummaryResponse(total=total, items=items)
