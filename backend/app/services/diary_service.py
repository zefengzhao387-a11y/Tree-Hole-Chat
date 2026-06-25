"""
日记管理业务逻辑
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from app.models.diary import Diary
from app.models.emotion_analysis import EmotionAnalysis


def _parse_inclusive_date_range(start_date: str, end_date: str) -> tuple[datetime, datetime]:
    """将 YYYY-MM-DD 转为含首尾全天的查询区间 [start, end+1day)"""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_exclusive = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    return start_dt, end_exclusive


async def get_diaries(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    page_size: int = 20,
    mood_label: str | None = None,
    sentiment: str | None = None,
) -> tuple[list[Diary], int]:
    query = (
        select(Diary)
        .options(selectinload(Diary.emotion_analysis))
        .where(Diary.user_id == user_id)
    )

    if mood_label:
        query = query.where(Diary.mood_label == mood_label)

    if sentiment:
        query = query.join(Diary.emotion_analysis).where(EmotionAnalysis.sentiment == sentiment)

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(desc(Diary.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    return list(result.unique().scalars().all()), total


async def get_diary_by_id(db: AsyncSession, diary_id: int, user_id: int) -> Diary | None:
    query = (
        select(Diary)
        .options(selectinload(Diary.emotion_analysis))
        .where(Diary.id == diary_id, Diary.user_id == user_id)
    )
    result = await db.execute(query)
    return result.unique().scalar_one_or_none()


async def create_diary(
    db: AsyncSession,
    user_id: int,
    title: str,
    content: str,
    mood_label: str | None = None,
) -> Diary:
    diary = Diary(user_id=user_id, title=title, content=content, mood_label=mood_label)
    db.add(diary)
    await db.commit()
    return diary


async def update_diary(
    db: AsyncSession,
    diary_id: int,
    user_id: int,
    title: str | None = None,
    content: str | None = None,
    mood_label: str | None = None,
) -> Diary | None:
    diary = await get_diary_by_id(db, diary_id, user_id)
    if not diary:
        return None

    if title is not None:
        diary.title = title
    if content is not None:
        diary.content = content
    if mood_label is not None:
        diary.mood_label = mood_label

    await db.commit()
    return diary


async def delete_diary(db: AsyncSession, diary_id: int, user_id: int) -> bool:
    diary = await get_diary_by_id(db, diary_id, user_id)
    if not diary:
        return False
    await db.delete(diary)
    await db.commit()
    return True


async def get_diaries_in_range(
    db: AsyncSession,
    user_id: int,
    start_date: str,
    end_date: str,
) -> list[Diary]:
    start_dt, end_exclusive = _parse_inclusive_date_range(start_date, end_date)
    query = (
        select(Diary)
        .options(selectinload(Diary.emotion_analysis))
        .where(
            Diary.user_id == user_id,
            Diary.created_at >= start_dt,
            Diary.created_at < end_exclusive,
        )
        .order_by(Diary.created_at)
    )
    result = await db.execute(query)
    return list(result.unique().scalars().all())
