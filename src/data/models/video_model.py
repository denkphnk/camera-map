import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Video(Base):
    __tablename__ = "video"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    duration: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    video_resolution: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    fps: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    time_of_day: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    tracing: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Run",
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    camera_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("d_camera.id"),
        nullable=False,
        index=True,
    )

    counter: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    file_object_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
