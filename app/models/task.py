from sqlalchemy import String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="Medium"
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


    user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"),
    nullable=False
    )

    user: Mapped["User"] = relationship(
    back_populates="tasks"
    )