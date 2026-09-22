from pydantic import BaseModel, ConfigDict

from src.data.models.analysis_model import AnalysisStatus

from datetime import datetime
from uuid import UUID


class AnalysisResponse(BaseModel):
    id: UUID
    video_id: UUID
    video_name: str
    camera_name: str
    status: AnalysisStatus
    result: dict | None
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class AnalysisFilters(BaseModel):
    status: AnalysisStatus | None = None
    video_id: UUID | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    camera_id: UUID | None = None


class AnalysisListResponse(BaseModel):
    items: list[AnalysisResponse]