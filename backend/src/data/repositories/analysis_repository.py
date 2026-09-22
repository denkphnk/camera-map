from uuid import UUID

from sqlalchemy import select, update, func

from src.data.repositories.base_repository import BaseRepository
from src.data.models.analysis_model import Analysis, AnalysisStatus
from src.data.models.video_model import Video

class AnalysisRepository(BaseRepository[Analysis]):
    def __init__(self, session):
        super().__init__(Analysis, session)

    async def get_by_video_id(self, video_id: UUID) -> Analysis | None:
        query = (
            select(self.model)
            .where(self.model.video_id == video_id)
        )

        analysis = await self.session.execute(query)
        return analysis.scalar_one_or_none()

    async def get_all(
    self,
    offset: int = 0,
    limit: int = 100,
    **filters,
    ) -> list[Analysis]:
        query = (
            select(self.model)
            .join(Video, self.model.video_id == Video.id)
        )

        if filters.get("status") is not None:
            query = query.where(
                self.model.status == filters["status"]
            )

        if filters.get("video_id") is not None:
            query = query.where(
                self.model.video_id == filters["video_id"]
            )

        if filters.get("camera_id") is not None:
            query = query.where(
                Video.camera_id == filters["camera_id"]
            )

        if filters.get("created_from") is not None:
            query = query.where(
                self.model.created_at >= filters["created_from"]
            )

        if filters.get("created_to") is not None:
            query = query.where(
                self.model.created_at <= filters["created_to"]
            )

        query = (
            query
            .order_by(self.model.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        return result.scalars().all()

    async def set_processing(self, id: UUID) -> Analysis | None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(
                {
                    "status": AnalysisStatus.PROCESSING,
                    "started_at": func.now()
                }
            )
            .returning(self.model)
        )

        analysis = await self.session.execute(query)
        return analysis.scalar_one_or_none()


    async def set_done(self, id: UUID, result: dict) -> Analysis | None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(
                {
                    "status": AnalysisStatus.DONE,
                    "result": result,
                    "finished_at": func.now()
                }
            )
            .returning(self.model)
        )

        analysis = await self.session.execute(query)
        return analysis.scalar_one_or_none()


    async def set_error(self, id: UUID, error: str) -> Analysis | None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(
                {
                    "status": AnalysisStatus.ERROR,
                    "error_message": error,
                    "finished_at": func.now()
                }
            )
            .returning(self.model)
        )

        analysis = await self.session.execute(query)
        return analysis.scalar_one_or_none()