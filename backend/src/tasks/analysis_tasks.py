from uuid import UUID

from celery import shared_task

from src.core.database import AsyncSessionLocal
from src.domain.services.analysis_service import AnalysisService


@shared_task
async def run_analysis_task(analysis_id: str):
    async with AsyncSessionLocal() as session:
        analysis_service = AnalysisService(session)

        await analysis_service.run_analysis(UUID(analysis_id))