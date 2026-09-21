from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VideoResponse(BaseModel):
    id: UUID
    name: str

    duration: float | None
    video_resolution: str | None
    fps: float | None

    time_of_day: str
    tracing: str

    author_id: UUID
    author_name: str | None = None

    counter: int

    file_size: int
    content_type: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VideoSearchFilters(BaseModel):
    name: str | None = None
    author_id: UUID | None = None
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class VideoListResponse(BaseModel):
    items: list[VideoResponse]
    total: int


class VideoDetailsResponse(VideoResponse):
    video_url: str
    preview_url: str | None
