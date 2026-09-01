import secrets
import uuid
import datetime

from hashlib import sha256
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError

from src.core.config import Settings


class TokenService:
    def __init__(self, settings: Settings):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def hash_refresh_token(self, refresh_token: str) -> str:
        token_bytes = refresh_token.encode("utf-8")
        hash_object = sha256(token_bytes)
        token_hash = hash_object.hexdigest()

        return token_hash

    def create_refresh_token(self) -> str:
        refresh_token = secrets.token_urlsafe(32)

        return refresh_token

    def create_access_token(self, user_id: uuid.UUID) -> str:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        exp_time = current_time + datetime.timedelta(
            minutes=self.access_token_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": current_time,
            "exp": exp_time,
        }

        access_token = jwt.encode(payload, self.secret_key, self.algorithm)

        return access_token

    def decode_access_token(self, token: str) -> uuid.UUID:
        try:
            decoded_token = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
        except ExpiredSignatureError:
            raise ValueError("Access token has expired")
        except JWTError:
            raise ValueError("Invalid access token")

        sub = decoded_token.get("sub")
        if not sub:
            raise ValueError("Missing token subject")

        token_type = decoded_token.get("type")
        if token_type != "access":
            raise ValueError("Wrong token type")

        try:
            user_id = uuid.UUID(sub)
        except ValueError as e:
            raise ValueError("Invalid user_id in token") from e

        return user_id
