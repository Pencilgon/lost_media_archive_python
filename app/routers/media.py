from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import MediaEntry, MediaCollection
from ..schemas import (
    MediaCreate,
    MediaUpdate,
    MediaResponse,
)

router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


@router.post(
    "",
    response_model=MediaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_media(
    data: MediaCreate,
    db: Session = Depends(get_db),
):
    # Check whether the collection exists
    if data.collection_id is not None:
        collection = db.get(
            MediaCollection,
            data.collection_id,
        )

        if collection is None:
            raise HTTPException(
                status_code=404,
                detail="Collection not found",
            )

    media_data = data.model_dump()

    if media_data["source_url"] is not None:
        media_data["source_url"] = str(media_data["source_url"])

    entry = MediaEntry(**media_data)

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


@router.get(
    "",
    response_model=list[MediaResponse],
)
def get_media(
    db: Session = Depends(get_db),
):
    statement = select(MediaEntry).order_by(MediaEntry.id)

    return list(db.scalars(statement).all())


@router.get(
    "/{media_id}",
    response_model=MediaResponse,
)
def get_media_by_id(
    media_id: int,
    db: Session = Depends(get_db),
):
    entry = db.get(MediaEntry, media_id)

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    return entry


@router.patch(
    "/{media_id}",
    response_model=MediaResponse,
)
def update_media(
    media_id: int,
    data: MediaUpdate,
    db: Session = Depends(get_db),
):
    entry = db.get(MediaEntry, media_id)

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    update_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    # Validate the new collection ID if supplied
    if "collection_id" in update_data:
        collection = db.get(
            MediaCollection,
            update_data["collection_id"],
        )

        if collection is None:
            raise HTTPException(
                status_code=404,
                detail="Collection not found",
            )

    # Convert HttpUrl into a regular string
    if update_data.get("source_url") is not None:
        update_data["source_url"] = str(
            update_data["source_url"]
        )

    for key, value in update_data.items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)

    return entry


@router.delete(
    "/{media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
):
    entry = db.get(MediaEntry, media_id)

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    db.delete(entry)
    db.commit()