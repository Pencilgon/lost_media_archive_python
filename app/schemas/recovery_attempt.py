from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecoveryAttemptCreate(BaseModel):
    success: bool = False

    notes: str | None = Field(
        default=None,
        max_length=2000,
    )


class RecoveryAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    media_id: int
    success: bool
    notes: str | None
    attempted_at: datetime