from uuid import UUID

from sqlalchemy import select, update, func

from src.data.repositories.base_repository import BaseRepository
from src.data.models.analysis_model import Analysis, AnalysisStatus

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