from src.domain.services.password_service import PasswordService


def test_hash_password():
    service = PasswordService()

    password_hash = service.hash_password("qwerty123")

    assert password_hash != "qwerty123"
    assert isinstance(password_hash, str)


def test_verify_password_success():
    service = PasswordService()

    password_hash = service.hash_password("qwerty123")

    assert service.verify_password(
        "qwerty123",
        password_hash,
    ) is True


def test_verify_password_wrong_password():
    service = PasswordService()

    password_hash = service.hash_password("qwerty123")

    assert service.verify_password(
        "wrong_password",
        password_hash,
    ) is False