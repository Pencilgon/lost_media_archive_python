from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class MediaType(str, Enum):
    MOVIE = "movie"
    GAME = "game"
    MUSIC = "music"
    BOOK = "book"
    VIDEO = "video"
    OTHER = "other"


class RecoveryStatus(str, Enum):
    LOST = "lost"
    PARTIALLY_RECOVERED = "partially_recovered"
    FOUND = "found"
    UNDER_INVESTIGATION = "under_investigation"


class MediaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    media_type: MediaType

    release_year: int | None = Field(
        default=None,
        ge=1800,
        le=2100,
    )

    recovery_status: RecoveryStatus = RecoveryStatus.LOST

    description: str | None = None

    source_url: HttpUrl | None = None

    collection_id: int | None = None


class MediaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)

    media_type: MediaType | None = None

    release_year: int | None = Field(
        default=None,
        ge=1800,
        le=2100,
    )

    recovery_status: RecoveryStatus | None = None

    description: str | None = None

    source_url: HttpUrl | None = None

    collection_id: int | None = None


class MediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    media_type: MediaType
    release_year: int | None
    recovery_status: RecoveryStatus
    description: str | None
    source_url: str | None
    collection_id: int | None