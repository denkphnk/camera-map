import uuid

import pytest

from src.core.config import settings
from src.domain.services.token_service import TokenService


@pytest.fixture
def token_service():
    return TokenService(settings)


def test_create_refresh_token(token_service):
    token = token_service.create_refresh_token()

    assert isinstance(token, str)
    assert len(token) > 0


def test_hash_refresh_token(token_service):
    token = "my_refresh_token"

    hash1 = token_service.hash_refresh_token(token)
    hash2 = token_service.hash_refresh_token(token)

    assert hash1 == hash2
    assert hash1 != token


def test_create_and_decode_access_token(token_service):
    user_id = uuid.uuid4()

    token = token_service.create_access_token(user_id)

    decoded_user_id = token_service.decode_access_token(token)

    assert decoded_user_id == user_id


def test_decode_invalid_token(token_service):
    with pytest.raises(
        ValueError,
        match="Invalid access token",
    ):
        token_service.decode_access_token(
            "invalid_token"
        )