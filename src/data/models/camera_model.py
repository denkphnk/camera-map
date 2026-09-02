import uuid

from sqlalchemy import DateTime, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime, timezone

from src.core.database import Base


class DCamera(Base):
    __tablename__ = 'd_camera'

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    camera_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    camera_name: Mapped[str] = mapped_column(String(255), nullable=False)
    camera_place: Mapped[str] = mapped_column(String(500), nullable=True)
    camera_place_cd: Mapped[int] = mapped_column(nullable=True)
    camera_latitude: Mapped[float] = mapped_column(nullable=False)
    camera_longitude: Mapped[float] = mapped_column(nullable=False)
    camera_type: Mapped[str] = mapped_column(String(100), nullable=True)
    camera_type_cd: Mapped[int] = mapped_column(nullable=True)
    camera_class: Mapped[str] = mapped_column(String(100), nullable=True)
    camera_class_cd: Mapped[int] = mapped_column(nullable=True)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    azimuth: Mapped[int] = mapped_column(nullable=True)
    archive: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    process_dttm: Mapped[datetime] =  mapped_column(DateTime(timezone=True), nullable=False, default=func.now())