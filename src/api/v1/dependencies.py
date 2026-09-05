from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from src.core.config import settings
from src.core.database import get_db
from src.core.cache import get_redis
from src.domain.services.auth_service import AuthService
from src.domain.services.camera_service import CameraService

async def get_auth_service(
    session: AsyncSession = Depends(get_db),
) -> AuthService:
    return AuthService(session, settings)


async def get_camera_service(
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
) -> CameraService:
    return CameraService(session=session, redis=redis)