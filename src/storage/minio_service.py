import io
import uuid
from datetime import timedelta

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from src.core.config import settings


class MinioService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

        self.bucket_name = settings.MINIO_BUCKET_NAME

    def create_bucket_if_not_exists(self) -> None:
        exists = self.client.bucket_exists(self.bucket_name)

        if not exists:
            self.client.make_bucket(self.bucket_name)

    async def upload_file(
        self,
        file: UploadFile,
        object_name: str | None = None,
        expires_days: int = 7,
    ) -> dict[str, str]:
        if object_name is None:
            extension = ""

            if file.filename and "." in file.filename:
                extension = f".{file.filename.rsplit('.', 1)[-1]}"

            object_name = f"{uuid.uuid4()}{extension}"

        content = await file.read()

        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=io.BytesIO(content),
            length=len(content),
            content_type=file.content_type,
        )

        url = self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            expires=timedelta(days=expires_days),
        )

        return {
            "object_name": object_name,
            "url": url,
        }

    def delete_file(self, object_name: str) -> None:
        self.client.remove_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
        )

    def get_presigned_url(
        self,
        object_name: str,
        expires_days: int = 7,
    ) -> str:
        return self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            expires=timedelta(days=expires_days),
        )

    def get_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(
                self.bucket_name,
                object_name,
            )

            data = response.read()

            response.close()
            response.release_conn()

            return data

        except S3Error as e:
            raise ValueError(f"Failed to get file: {e}") from e