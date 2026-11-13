from datetime import datetime

from sqlalchemy import (
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class RecoveryAttempt(Base):
    __tablename__ = "recovery_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)

    media_id: Mapped[int] = mapped_column(
        ForeignKey(
            "media_entries.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    media: Mapped["MediaEntry"] = relationship(
        back_populates="recovery_attempts",
    )