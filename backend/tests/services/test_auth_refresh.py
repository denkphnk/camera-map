import pytest

from src.core.config import settings
from src.domain.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_refresh_success(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    await service.register(
        email="refresh@test.com",
        full_name="Refresh User",
        password="password123",
    )

    login_tokens = await service.login(
        email="refresh@test.com",
        password="password123",
    )

    new_tokens = await service.refresh(
        login_tokens["refresh_token"]
    )

    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens

    assert (
        new_tokens["refresh_token"]
        != login_tokens["refresh_token"]
    )


@pytest.mark.asyncio
async def test_refresh_invalid_token(
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
        await service.refresh(
            "invalid_token"
        )