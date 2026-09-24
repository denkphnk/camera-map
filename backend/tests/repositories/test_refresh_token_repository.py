from datetime import UTC, datetime, timedelta

import pytest

from src.data.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from src.data.repositories.user_repository import (
    UserRepository,
)


@pytest.mark.asyncio
async def test_get_by_hash(
    db_session,
):
    user_repo = UserRepository(
        db_session,
    )

    token_repo = RefreshTokenRepository(
        db_session,
    )

    user = await user_repo.create(
        {
            "email": "token@test.com",
            "full_name": "Token User",
            "password_hash": "hash",
        }
    )

    token = await token_repo.create(
        {
            "user_id": user.id,
            "token_hash": "hash123",
            "expires_at": (
                datetime.now(UTC)
                + timedelta(days=7)
            ),
        }
    )

    await db_session.commit()

    found_token = await token_repo.get_by_hash(
        "hash123"
    )

    assert found_token is not None
    assert found_token.id == token.id


@pytest.mark.asyncio
async def test_revoke_token(
    db_session,
):
    user_repo = UserRepository(
        db_session,
    )

    token_repo = RefreshTokenRepository(
        db_session,
    )

    user = await user_repo.create(
        {
            "email": "revoke@test.com",
            "full_name": "Revoke User",
            "password_hash": "hash",
        }
    )

    await token_repo.create(
        {
            "user_id": user.id,
            "token_hash": "revoke_hash",
            "expires_at": (
                datetime.now(UTC)
                + timedelta(days=7)
            ),
        }
    )

    await db_session.commit()

    revoked_token = await token_repo.revoke(
        "revoke_hash"
    )

    await db_session.commit()

    assert revoked_token is not None
    assert revoked_token.revoked_at is not None