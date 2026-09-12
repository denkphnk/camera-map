from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.api.v1.videos.videos_schemas import VideoResponse


class UserProfileResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    videos: list[VideoResponse]
    total_videos: int
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    full_name: str | None = None