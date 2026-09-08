from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cache import get_redis
from src.core.config import settings
from src.core.database import get_db
from src.storage.minio_service import MinioService
from src.domain.services.auth_service import AuthService
from src.domain.services.camera_service import CameraService
from src.domain.services.videos_service import VideoService

async def get_auth_service(
    session: AsyncSession = Depends(get_db),
) -> AuthService:
    return AuthService(session, settings)


async def get_camera_service(
    session: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)
) -> CameraService:
    return CameraService(session=session, redis=redis)


def get_minio_service() -> MinioService:
    return MinioService()

async def get_video_service(
    session: AsyncSession = Depends(get_db), minio_service: MinioService = Depends(get_minio_service)
) -> VideoService:
    return VideoService(session=session, minio_service=minio_service)