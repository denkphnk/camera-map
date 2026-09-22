from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.v1.dependencies import get_analysis_service
from src.api.v1.analysis.analysis_schemas import AnalysisResponse, AnalysisListResponse, AnalysisFilters
from src.domain.services.analysis_service import AnalysisService

analysis_router = APIRouter(prefix="/api/v1/analyses", tags=["analysis"])

@analysis_router.get("/", response_model=AnalysisListResponse)
async def get_all_analyses(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    filters: AnalysisFilters = Depends(),
    service: AnalysisService = Depends(get_analysis_service)
):
    analyses = await service.get_all(filters, offset, limit)
    return AnalysisListResponse(items=analyses)


@analysis_router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_by_id(
    analysis_id: UUID,
    service: AnalysisService = Depends(get_analysis_service),
):
    analysis = await service.get_by_id(analysis_id)

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    return analysis