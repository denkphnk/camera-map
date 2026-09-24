import pytest

from src.core.config import settings
from src.domain.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_logout_success(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    await service.register(
        email="logout@test.com",
        full_name="Logout User",
        password="password123",
    )

    tokens = await service.login(
        email="logout@test.com",
        password="password123",
    )

    await service.logout(
        tokens["refresh_token"]
    )


@pytest.mark.asyncio
async def test_logout_invalid_token(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    with pytest.raises(
        ValueError,
        match="Refresh token not found",
    ):
        await service.logout(
            "invalid_token"
        )