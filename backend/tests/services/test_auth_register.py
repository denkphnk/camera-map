import pytest

from src.core.config import settings
from src.domain.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_register_success(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    user = await service.register(
        email="register@test.com",
        full_name="Test User",
        password="password123",
    )

    assert user.id is not None
    assert user.email == "register@test.com"
    assert user.full_name == "Test User"
    assert user.password_hash != "password123"


@pytest.mark.asyncio
async def test_register_duplicate_email(
    db_session,
):
    service = AuthService(
        session=db_session,
        settings=settings,
    )

    await service.register(
        email="duplicate@test.com",
        full_name="User One",
        password="password123",
    )

    with pytest.raises(
        ValueError,
        match="already exists",
    ):
        await service.register(
            email="duplicate@test.com",
            full_name="User Two",
            password="password123",
        )