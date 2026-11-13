from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import MediaCollection, MediaEntry
from ..schemas import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
    MediaResponse,
)

router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
)


@router.post(
    "",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection(
    data: CollectionCreate,
    db: Session = Depends(get_db),
):
    collection = MediaCollection(**data.model_dump())

    db.add(collection)

    try:
        db.commit()
        db.refresh(collection)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A collection with this name already exists",
        )

    return collection


@router.get(
    "",
    response_model=list[CollectionResponse],
)
def get_collections(
    db: Session = Depends(get_db),
):
    statement = select(MediaCollection).order_by(MediaCollection.id)

    return list(db.scalars(statement).all())


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
):
    collection = db.get(MediaCollection, collection_id)

    if collection is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found",
        )

    return collection


@router.patch(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def update_collection(
    collection_id: int,
    data: CollectionUpdate,
    db: Session = Depends(get_db),
):
    collection = db.get(MediaCollection, collection_id)

    if collection is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found",
        )

    update_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for key, value in update_data.items():
        setattr(collection, key, value)

    try:
        db.commit()
        db.refresh(collection)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A collection with this name already exists",
        )

    return collection


@router.delete(
    "/{collection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
):
    collection = db.get(MediaCollection, collection_id)

    if collection is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found",
        )

    db.delete(collection)
    db.commit()


@router.get(
    "/{collection_id}/media",
    response_model=list[MediaResponse],
)
def get_collection_media(
    collection_id: int,
    db: Session = Depends(get_db),
):
    collection = db.get(MediaCollection, collection_id)

    if collection is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found",
        )

    statement = (
        select(MediaEntry)
        .where(MediaEntry.collection_id == collection_id)
        .order_by(MediaEntry.id)
    )

    return list(db.scalars(statement).all())