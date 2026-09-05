from pydantic import BaseModel

class CameraSearchFilters(BaseModel):
    search: str | None
    model: str | None
    camera_type: str | None
    camera_class: str | None
    video_count_from: int | None
    video_count_to: int | None
