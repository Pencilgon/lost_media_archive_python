from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class MediaEntry(Base):
    __tablename__ = "media_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    media_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    release_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    recovery_status: Mapped[str] = mapped_column(
        String(30),
        default="lost",
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Relationship with MediaCollection
    collection_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "media_collections.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    collection: Mapped["MediaCollection | None"] = relationship(
        back_populates="media_entries",
    )

    # Relationship with RecoveryAttempt
    recovery_attempts: Mapped[list["RecoveryAttempt"]] = relationship(
        back_populates="media",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )