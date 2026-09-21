import uuid
import re
from pathlib import Path

from fastapi import UploadFile

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.domain.schemas.video_schemas import VideoDetailsResponse, VideoResponse
from src.data.models.video_model import Video
from src.data.repositories.video_repository import VideoRepository
from src.data.repositories.user_repository import UserRepository
from src.data.repositories.camera_repository import CameraRepository
from src.storage.minio_service import MinioService
from src.tasks.video_tasks import process_video


class VideoService:
    def __init__(
        self,
        session: AsyncSession,
        minio_service: MinioService,
        redis: Redis
    ):
        self.session = session
        self.redis = redis
        self.video_repo = VideoRepository(session)
        self.user_repo = UserRepository(session)
        self.camera_repo = CameraRepository(session)
        self.minio_service = minio_service

    async def get_video_by_id(self, video_id: uuid.UUID) -> Video | None:
        return await self.video_repo.get_by_id(video_id)

    async def get_videos_by_author(
        self,
        author_id: uuid.UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Video], int]:
        return await self.video_repo.get_by_author(
            author_id=author_id,
            offset=offset,
            limit=limit,
        )

    async def get_videos_by_camera(
        self,
        camera_id: uuid.UUID,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Video], int]:
        return await self.video_repo.get_by_camera(
            camera_id=camera_id,
            offset=offset,
            limit=limit,
        )

    async def search_videos(
        self,
        name: str | None = None,
        author_id: uuid.UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Video], int]:
        return await self.video_repo.search(
            name=name,
            author_id=author_id,
            offset=offset,
            limit=limit,
        )

    async def increment_counter(self, video_id: uuid.UUID) -> Video | None:
        video = await self.video_repo.increment_counter(video_id)

        if video:
            await self.session.commit()

        return video

    async def delete_video(self, video_id: uuid.UUID) -> bool:
        video = await self.video_repo.get_by_id(video_id)

        if not video:
            return False


        deleted = await self.video_repo.delete(video_id)

        if deleted:
            await self.session.commit()

            if video.file_object_key:
                self.minio_service.delete_file(
                    object_name=video.file_object_key,
                )

            if video.preview_object_key:
                self.minio_service.delete_file(
                    object_name=video.preview_object_key,
                )

            await self.redis.delete("cameras:geojson")


        return deleted

    async def upload_video(
        self,
        file: UploadFile,
        name: str,
        author_id: uuid.UUID,
        camera_id: uuid.UUID
    ) -> Video:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix != '.mp4':
            raise ValueError('Only .mp4 files are allowed')

        author_exists = await self.user_repo.exists_by_id(author_id)
        if not author_exists:
            raise ValueError("Author not found")

        camera_exists = await self.camera_repo.exists_by_id(camera_id)
        if not camera_exists:
            raise ValueError("Camera not found")

        uploaded_object_name = None

        contents = await file.read()
        if not contents:
            raise ValueError("Empty file")
        
        try:
            await file.seek(0)
            file_uuid = uuid.uuid4()
            object_key = f"videos/{file_uuid}{suffix}"

            minio_data = await self.minio_service.upload_file(
                file=file,
                object_name=object_key,
            )
            uploaded_object_name = minio_data["object_name"]

            match = re.search(
                r"\d{2}\.\d{2}\.\d{4}_(\d{2})\.\d{2}\.\d{2}",
                name,
            )
            if not match:
                raise ValueError(
                    "Cannot determine time_of_day from filename"
                )
            hour = int(match.group(1))
            time_of_day = self._get_time_of_day(hour)


            video = await self.video_repo.create(
                {
                    "name": name,
                    "duration": 0,
                    "video_resolution": "",
                    "fps": 0,
                    "time_of_day": time_of_day,
                    "tracing": "queued",
                    "author_id": author_id,
                    "counter": 0,
                    "file_object_key": uploaded_object_name,
                    "file_size": len(contents),
                    "content_type": file.content_type,
                    "preview_object_key": "",
                    "camera_id": camera_id
                }
            )

            await self.session.commit()
            await self.session.refresh(video)

            process_video.delay(str(video.id))

            await self.redis.delete("cameras:geojson")


            return video

        except Exception:
            await self.session.rollback()
            if uploaded_object_name:
                self.minio_service.delete_file(uploaded_object_name)

            raise


    async def get_video_details(self, video_id: uuid.UUID) -> VideoDetailsResponse | None:
        video = await self.video_repo.get_by_id(video_id)

        if video is None:
            return None

        return VideoDetailsResponse(
            **VideoResponse.model_validate(video).model_dump(),
            video_url=f"http://{settings.BASE_URL}/videos/{video.id}/stream",
            preview_url=f"http://{settings.BASE_URL}/videos/{video.id}/preview",
        )

    async def get_video_file(self, video_id: uuid.UUID) -> tuple[bytes, str] | None:
        video = await self.video_repo.get_by_id(video_id)

        if video is None:
            return None

        file_data = self.minio_service.get_file(video.file_object_key)

        return file_data, video.content_type

    async def get_preview_file(self, video_id: uuid.UUID) -> bytes | None:
        video = await self.video_repo.get_by_id(video_id)

        if video is None:
            return None

        return self.minio_service.get_file(video.preview_object_key)

    def _get_time_of_day(self, hour: int) -> str:
        if 0 <= hour < 6:
            return 'night'
        elif 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'day'
        elif 18 <= hour  < 24:
            return 'evening'
        raise ValueError('Invalid time format')
        