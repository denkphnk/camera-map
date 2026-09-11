from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.user_model import User
from src.domain.services.user_service import UserService
from src.data.repositories.user_repository import UserRepository
from src.domain.services.token_service import TokenService
from src.core.cache import get_redis
from src.core.config import settings
from src.core.database import get_db
from src.storage.minio_service import MinioService
from src.domain.services.auth_service import AuthService
from src.domain.services.camera_service import CameraService
from src.domain.services.videos_service import VideoService


security = HTTPBearer()

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
    session: AsyncSession = Depends(get_db), minio_service: MinioService = Depends(get_minio_service), redis: Redis = Depends(get_redis)
) -> VideoService:
    return VideoService(session=session, minio_service=minio_service, redis=redis)

async def get_user_service(
    session: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(session)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db),
) -> User:
    try:
        user_id = TokenService(settings).decode_access_token(
            credentials.credentials
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    user = await UserRepository(session).get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user