from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import MediaEntry, RecoveryAttempt
from ..schemas import (
    RecoveryAttemptCreate,
    RecoveryAttemptResponse,
)

router = APIRouter(
    prefix="/attempts",
    tags=["Recovery Attempts"],
)


@router.post(
    "/media/{media_id}/attempts",
    response_model=RecoveryAttemptResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_recovery_attempt(
    media_id: int,
    data: RecoveryAttemptCreate,
    db: Session = Depends(get_db),
):
    media = db.get(MediaEntry, media_id)

    if media is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    attempt = RecoveryAttempt(
        media_id=media_id,
        **data.model_dump(),
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


@router.get(
    "/media/{media_id}/attempts",
    response_model=list[RecoveryAttemptResponse],
)
def get_media_attempts(
    media_id: int,
    db: Session = Depends(get_db),
):
    media = db.get(MediaEntry, media_id)

    if media is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    statement = (
        select(RecoveryAttempt)
        .where(RecoveryAttempt.media_id == media_id)
        .order_by(RecoveryAttempt.id)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{attempt_id}",
    response_model=RecoveryAttemptResponse,
)
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = db.get(RecoveryAttempt, attempt_id)

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Recovery attempt not found",
        )

    return attempt


@router.delete(
    "/{attempt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = db.get(RecoveryAttempt, attempt_id)

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Recovery attempt not found",
        )

    db.delete(attempt)
    db.commit()