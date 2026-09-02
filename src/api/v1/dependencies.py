from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.config import settings
from src.core.database import get_db
from src.domain.services.auth_service import AuthService


async def get_auth_service(
    session: AsyncSession = Depends(get_db),
) -> AuthService:
    return AuthService(session, settings)