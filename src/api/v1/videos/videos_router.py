from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from src.api.v1.videos.videos_schemas import (
    VideoListResponse,
    VideoResponse,
    VideoSearchFilters,
)
from src.api.v1.dependencies import get_video_service
from src.domain.services.videos_service import VideoService

videos_router = APIRouter(prefix="/videos", tags=["Video"])


@videos_router.get("/", response_model=VideoListResponse)
async def get_videos(
    data: VideoSearchFilters = Depends(),
    service: VideoService = Depends(get_video_service),
):
    videos, total = await service.search_videos(
        name=data.name, author_id=data.author_id, offset=data.offset, limit=data.limit
    )

    return VideoListResponse(items=videos, total=total)


@videos_router.get("/author/{author_id}", response_model=VideoListResponse)
async def get_videos_by_author(
    author_id: UUID,
    offset: int = 0,
    limit: int = 20,
    service: VideoService = Depends(get_video_service),
):
    videos, total = await service.get_videos_by_author(
        author_id=author_id, offset=offset, limit=limit
    )

    return VideoListResponse(items=videos, total=total)


@videos_router.post("/{video_id}/increment-counter", response_model=VideoResponse)
async def increment_counter(
    video_id: UUID, service: VideoService = Depends(get_video_service)
):
    video = await service.increment_counter(video_id)
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    return video


@videos_router.get("/{video_id}", response_model=VideoResponse)
async def get_video_by_id(
    video_id: UUID, service: VideoService = Depends(get_video_service)
):
    video = await service.get_video_by_id(video_id)

    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    return video


@videos_router.delete('/{video_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: UUID, service: VideoService = Depends(get_video_service)):
    deleted = await service.delete_video(video_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

@videos_router.post(
    "/upload",
    response_model=VideoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_video(
    file: UploadFile = File(...),
    name: str = Form(...),
    author_id: UUID = Form(...),
    service: VideoService = Depends(get_video_service),
):
    try:
        return await service.upload_video(
            file=file,
            name=name,
            author_id=author_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )