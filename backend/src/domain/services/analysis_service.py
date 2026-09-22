import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID
from random import randint

from src.data.models.analysis_model import Analysis
from src.data.repositories.analysis_repository import AnalysisRepository
from src.data.repositories.video_repository import VideoRepository
from src.domain.schemas.analysis_schemas import AnalysisFilters, AnalysisResponse


class AnalysisService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.analysis_repo = AnalysisRepository(session)
        self.video_repo = VideoRepository(session)

    async def get_by_id(self, analysis_id: UUID) -> Analysis | None:
        analysis = await self.analysis_repo.get_by_id(analysis_id)
        return analysis

    async def get_by_video_id(self, video_id: UUID) -> Analysis | None:
        analysis = await self.analysis_repo.get_by_video_id(video_id)
        return analysis

    async def get_all(self, filters: AnalysisFilters, offset: int = 0, limit: int = 20) -> list[Analysis]:
        items = []
        rows = await self.analysis_repo.get_all(offset, limit, **filters.model_dump(exclude_none=True))

        for analysis, video_name, camera_name in rows:
            items.append(
                AnalysisResponse(
                    id=analysis.id,
                    video_id=analysis.video_id,
                    status=analysis.status,
                    result=analysis.result,
                    error_message=analysis.error_message,
                    created_at=analysis.created_at,
                    started_at=analysis.started_at,
                    finished_at=analysis.finished_at,
                    video_name=video_name,
                    camera_name=camera_name,
                )
            )

        return items

    async def create(self, video_id: UUID) -> Analysis:
        exists = await self.video_repo.get_by_id(video_id)
        if not exists:
            raise ValueError("Video not found")

        analysis_exists = await self.analysis_repo.get_by_video_id(video_id)
        if analysis_exists:
            raise ValueError("Analysis already exists")

        analysis = await self.analysis_repo.create({"video_id": video_id})
        await self.session.commit()

        return analysis

    async def start_analysis(self, analysis_id: UUID) -> None:
        analysis = await self.analysis_repo.get_by_id(analysis_id)
        if not analysis:
            raise ValueError("Analysis not found")

        await self.analysis_repo.set_processing(analysis_id)
        await self.session.commit()

    async def finish_analysis(self, analysis_id: UUID, result: dict) -> None:
        analysis = await self.analysis_repo.get_by_id(analysis_id)
        if not analysis:
            raise ValueError("Analysis not found")
        
        await self.analysis_repo.set_done(analysis_id, result)
        await self.session.commit()

    async def fail_analysis(self, analysis_id: UUID, error: str) -> None:
        analysis = await self.analysis_repo.get_by_id(analysis_id)
        if not analysis:
            raise ValueError("Analysis not found")
        
        await self.analysis_repo.set_error(analysis_id, error)
        await self.session.commit()


    async def run_analysis(self, analysis_id: UUID) -> None:
        await self.start_analysis(analysis_id)
        error = 1 <= randint(1, 100) <= 10
        if error:
            await asyncio.sleep(3)
            await self.fail_analysis(analysis_id, "Analysis error")
            return
        
        await asyncio.sleep(10)
        await self.finish_analysis(analysis_id, {"tracks": [], "objects_count": 0})