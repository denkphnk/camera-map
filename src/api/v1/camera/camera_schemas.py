from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CameraSearchFilters(BaseModel):
    search: str | None = None
    model: str | None = None
    camera_type: str | None = None
    camera_class: str | None = None
    video_count_from: int | None = None
    video_count_to: int | None = None



class CameraResponse(BaseModel):
    id: UUID
    camera_id: str
    camera_name: str
    camera_place: str | None
    camera_place_cd: int | None
    camera_latitude: float
    camera_longitude: float
    camera_type: str | None
    camera_type_cd: int | None
    camera_class: str | None
    camera_class_cd: int | None
    model: str | None
    serial_number: str | None
    azimuth: int | None
    archive: int
    process_dttm: datetime

    model_config = ConfigDict(from_attributes=True)