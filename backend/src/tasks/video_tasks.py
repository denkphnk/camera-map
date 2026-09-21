import os
import tempfile
import uuid

from src.core.database import AsyncSessionLocal
from src.storage.minio_service import MinioService


from src.celery_app import celery_app
from src.data.repositories.video_repository import VideoRepository
from src.domain.services.video_metadata_service import VideoMetadataService


@celery_app.task(bind=True)
async def process_video(self, video_id: uuid.UUID):
    async with AsyncSessionLocal() as session:
        video_repo = VideoRepository(session)

        minio_service = MinioService()

        video_metadata_service = VideoMetadataService()

        try:
            uploaded_preview_object_name = None
            temp_path = None
            preview_path = None
            video = None

            video = await video_repo.get_by_id(video_id)
            if video is None:
                return

            exists_processing_video = await video_repo.exists_processing_video(
                video.author_id, video_id
            )
            if exists_processing_video:
                return

            await video_repo.update(video.id, {"tracing": "processing"})
            await session.commit()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp4",
            ) as temp_file:
                temp_path = temp_file.name

            minio_service.download_file(video.file_object_key, temp_path)

            metadata = video_metadata_service.get_metadata(temp_path)
            file_uuid = uuid.uuid4()
            preview_object_key = f"previews/{file_uuid}.jpg"

            preview_path = f"{temp_path}.jpg"

            video_metadata_service.extract_first_frame(
                video_path=temp_path,
                output_path=preview_path,
            )

            preview_data = minio_service.upload_local_file(
                file_path=preview_path,
                object_name=preview_object_key,
                content_type="image/jpeg",
            )

            uploaded_preview_object_name = preview_data["object_name"]

            await video_repo.update(
                video.id,
                {
                    "duration": metadata["duration"],
                    "video_resolution": metadata["resolution"],
                    "fps": metadata["fps"],
                    "tracing": "ready",
                    "preview_object_key": uploaded_preview_object_name,
                },
            )

            await session.commit()
        except Exception:
            await session.rollback()

            await video_repo.update(video_id, {"tracing": "error"})
            await session.commit()

            if uploaded_preview_object_name:
                minio_service.delete_file(uploaded_preview_object_name)

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

            if preview_path and os.path.exists(preview_path):
                os.remove(preview_path)

            if video:
                next_video = await video_repo.get_next_queued_video(video.author_id)
                if next_video:
                    process_video.delay(str(next_video.id))
