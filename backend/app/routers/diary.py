"""
日记管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.deps.auth import get_current_user
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse, DiaryListResponse, EmotionAnalysisBrief
from app.services import diary_service, emotion_analyzer
from app.rag.loader import load_diary_documents
from app.rag.splitter import split_documents
from app.rag.vector_store import update_diary_vectors, delete_diary_vectors

router = APIRouter(prefix="/api/diary", tags=["日记管理"])


def _to_response(diary, analysis=None) -> DiaryResponse:
    if analysis is None and diary.emotion_analysis:
        ea = diary.emotion_analysis
        analysis = EmotionAnalysisBrief(
            id=ea.id,
            primary_emotion=ea.primary_emotion,
            sentiment=ea.sentiment,
            intensity=ea.intensity,
            summary=ea.summary,
        )
    return DiaryResponse(
        id=diary.id,
        title=diary.title,
        content=diary.content,
        mood_label=diary.mood_label,
        created_at=diary.created_at,
        updated_at=diary.updated_at,
        emotion_analysis=analysis,
    )


@router.get("", response_model=DiaryListResponse)
async def list_diaries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    mood_label: str | None = Query(None),
    sentiment: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    diaries, total = await diary_service.get_diaries(
        db, user.id, page, page_size, mood_label, sentiment
    )
    return DiaryListResponse(total=total, items=[_to_response(d) for d in diaries])


@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(
    diary_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    diary = await diary_service.get_diary_by_id(db, diary_id, user.id)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")
    return _to_response(diary)


@router.post("", response_model=DiaryResponse, status_code=201)
async def create_diary(
    data: DiaryCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    diary = await diary_service.create_diary(db, user.id, data.title, data.content, data.mood_label)

    analysis = None
    analysis_obj = None
    try:
        analysis_obj = await emotion_analyzer.analyze_diary_emotion(db, diary)
    except Exception:
        pass

    try:
        docs = load_diary_documents(
            diary_id=diary.id,
            user_id=user.id,
            title=diary.title,
            content=diary.content,
            date=diary.created_at,
            primary_emotion=analysis_obj.primary_emotion if analysis_obj else None,
        )
        update_diary_vectors(diary.id, split_documents(docs))
    except Exception:
        pass

    if analysis_obj:
        analysis = EmotionAnalysisBrief(
            id=analysis_obj.id,
            primary_emotion=analysis_obj.primary_emotion,
            sentiment=analysis_obj.sentiment,
            intensity=analysis_obj.intensity,
            summary=analysis_obj.summary,
        )

    return _to_response(diary, analysis)


@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    data: DiaryUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    diary = await diary_service.update_diary(
        db, diary_id, user.id,
        title=data.title, content=data.content, mood_label=data.mood_label,
    )
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    analysis_obj = None
    try:
        analysis_obj = await emotion_analyzer.analyze_diary_emotion(db, diary)
    except Exception:
        pass

    try:
        docs = load_diary_documents(
            diary_id=diary.id,
            user_id=user.id,
            title=diary.title,
            content=diary.content,
            date=diary.created_at,
            primary_emotion=analysis_obj.primary_emotion if analysis_obj else None,
        )
        update_diary_vectors(diary.id, split_documents(docs))
    except Exception:
        pass

    analysis = None
    if analysis_obj:
        analysis = EmotionAnalysisBrief(
            id=analysis_obj.id,
            primary_emotion=analysis_obj.primary_emotion,
            sentiment=analysis_obj.sentiment,
            intensity=analysis_obj.intensity,
            summary=analysis_obj.summary,
        )

    return _to_response(diary, analysis)


@router.delete("/{diary_id}")
async def delete_diary(
    diary_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    success = await diary_service.delete_diary(db, diary_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="日记不存在")
    try:
        delete_diary_vectors(diary_id)
    except Exception:
        pass
    return {"message": "删除成功", "diary_id": diary_id}
