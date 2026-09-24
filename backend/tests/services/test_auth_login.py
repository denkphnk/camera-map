import pytest

from src.core.config import settings
from src.domain.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_login_success(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    await service.register(
        email="login@test.com",
        full_name="Login User",
        password="password123",
    )

    tokens = await service.login(
        email="login@test.com",
        password="password123",
    )

    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.asyncio
async def test_login_wrong_password(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    await service.register(
        email="wrong@test.com",
        full_name="Wrong User",
        password="password123",
    )

    with pytest.raises(
        ValueError,
        match="Invalid email or password",
    ):
        await service.login(
            email="wrong@test.com",
            password="wrong_password",
        )


@pytest.mark.asyncio
async def test_login_unknown_user(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    with pytest.raises(
        ValueError,
        match="Invalid email or password",
    ):
        await service.login(
            email="notfound@test.com",
            password="password123",
        )