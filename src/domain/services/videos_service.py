import os
import tempfile
import uuid
from pathlib import Path

from fastapi import UploadFile

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.services.video_metadata_service import VideoMetadataService
from src.domain.schemas.video_schemas import VideoDetailsResponse, VideoResponse
from src.data.models.video_model import Video
from src.data.repositories.video_repository import VideoRepository
from src.data.repositories.user_repository import UserRepository
from src.data.repositories.camera_repository import CameraRepository
from src.storage.minio_service import MinioService


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
        self.video_metadata_service = VideoMetadataService()

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
        author_exists = await self.user_repo.exists_by_id(author_id)
        if not author_exists:
            raise ValueError("Author not found")

        camera_exists = await self.camera_repo.exists_by_id(camera_id)
        if not camera_exists:
            raise ValueError("Camera not found")

        if not file.content_type or not file.content_type.startswith("video/"):
            raise ValueError("File must be a video")

        uploaded_object_name = None
        uploaded_preview_object_name = None
        temp_path = None
        preview_path = None
        suffix = Path(file.filename or "").suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            contents = await file.read()
            if not contents:
                raise ValueError("Empty file")
            temp_file.write(contents)
            temp_path = temp_file.name

        try:
            metadata = self.video_metadata_service.get_metadata(temp_path)
            await file.seek(0)
            file_uuid = uuid.uuid4()
            object_key = f"videos/{file_uuid}{suffix}"
            preview_object_key = f"previews/{file_uuid}.jpg"

            preview_path = f"{temp_path}.jpg"

            self.video_metadata_service.extract_first_frame(
                video_path=temp_path,
                output_path=preview_path,
            )

            minio_data = await self.minio_service.upload_file(
                file=file,
                object_name=object_key,
            )
            uploaded_object_name = minio_data["object_name"]

            preview_data = self.minio_service.upload_local_file(
                file_path=preview_path,
                object_name=preview_object_key,
                content_type="image/jpeg",
            )

            uploaded_preview_object_name = preview_data["object_name"]

            video = await self.video_repo.create(
                {
                    "name": name,
                    "duration": metadata["duration"],
                    "video_resolution": metadata["resolution"],
                    "fps": metadata["fps"],
                    "time_of_day": "day",
                    "tracing": "Run",
                    "author_id": author_id,
                    "counter": 0,
                    "file_object_key": uploaded_object_name,
                    "file_size": len(contents),
                    "content_type": file.content_type,
                    "preview_object_key": uploaded_preview_object_name,
                    "camera_id": camera_id
                }
            )

            await self.session.commit()
            await self.session.refresh(video)

            await self.redis.delete("cameras:geojson")


            return video

        except Exception:
            await self.session.rollback()
            if uploaded_object_name:
                self.minio_service.delete_file(uploaded_object_name)

            if uploaded_preview_object_name:
                self.minio_service.delete_file(uploaded_preview_object_name)
            raise

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

            if preview_path and os.path.exists(preview_path):
                os.remove(preview_path)


    async def get_video_details(self, video_id: uuid.UUID) -> VideoDetailsResponse | None:
        video = await self.video_repo.get_by_id(video_id)

        if video is None:
            return None

        return VideoDetailsResponse(
            **VideoResponse.model_validate(video).model_dump(),
            video_url=f"/api/v1/videos/{video.id}/stream",
            preview_url=f"/api/v1/videos/{video.id}/preview",
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