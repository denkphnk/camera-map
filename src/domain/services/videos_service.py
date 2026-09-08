from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.video_model import Video
from src.data.repositories.video_repository import VideoRepository
from src.storage.minio_service import MinioService
from src.core.config import settings


class VideoService:
    def __init__(
        self,
        session: AsyncSession,
        minio_service: MinioService,
    ):
        self.session = session
        self.video_repo = VideoRepository(session)
        self.minio_service = minio_service
        self.minio_bucket_name = settings.MINIO_BUCKET_NAME

    async def get_video_by_id(self, video_id: UUID) -> Video | None:
        return await self.video_repo.get_by_id(video_id)

    async def get_videos_by_author(
        self,
        author_id: UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Video], int]:
        return await self.video_repo.get_by_author(
            author_id=author_id,
            offset=offset,
            limit=limit,
        )

    async def search_videos(
        self,
        name: str | None = None,
        author_id: UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Video], int]:
        return await self.video_repo.search(
            name=name,
            author_id=author_id,
            offset=offset,
            limit=limit,
        )

    async def increment_counter(self, video_id: UUID) -> Video | None:
        video = await self.video_repo.increment_counter(video_id)

        if video:
            await self.session.commit()

        return video

    async def delete_video(self, video_id: UUID) -> bool:
        video = await self.video_repo.get_by_id(video_id)

        if not video:
            return False

        if video.file_object_key:
            self.minio_service.delete_file(
                bucket=self.minio_bucket_name,
                object_name=video.file_object_key,
            )

        deleted = await self.video_repo.delete(video_id)

        if deleted:
            await self.session.commit()

        return deleted