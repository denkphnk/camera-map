from sqlalchemy.ext.asyncio import AsyncSession

import datetime

from src.core.config import Settings
from src.data.repositories.refresh_token_repository import RefreshTokenRepository
from src.data.repositories.user_repository import UserRepository
from src.domain.services.token_service import TokenService
from src.domain.services.password_service import PasswordService

from src.data.models.user_model import User


class AuthService:
    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.refresh_repo = RefreshTokenRepository(session=session)
        self.user_repo = UserRepository(session)
        self.token_service = TokenService(settings)
        self.pwd_service = PasswordService()

    async def register(self, email: str, full_name: str, password: str) -> User:
        exists = await self.user_repo.exists_by_email(email)

        if exists:
            raise ValueError(f"User with email {email} already exists.")

        password_hash = self.pwd_service.hash_password(password)
        user = await self.user_repo.create(
            {"email": email, "full_name": full_name, "password_hash": password_hash}
        )

        await self.session.commit()
        return user

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_by_email(email)
        if user is None:
            raise ValueError("Invalid email or password")


        password_verified = self.pwd_service.verify_password(
            password, user.password_hash
        )
        if not password_verified:
            raise ValueError("Invalid email or password")

        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token()
        refresh_token_hash = self.token_service.hash_refresh_token(refresh_token)

        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=self.token_service.refresh_token_expire_days
        )

        await self.refresh_repo.create(
            {"user_id": user.id, "token_hash": refresh_token_hash, 'expires_at': expires_at}
        )

        await self.session.commit()

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def refresh(self, refresh_token: str) -> dict:
        refresh_token_hash = self.token_service.hash_refresh_token(refresh_token)
        stored_token = await self.refresh_repo.get_by_hash(refresh_token_hash)

        if stored_token is None:
            raise ValueError('Refresh token not found')

        if stored_token.revoked_at is not None:
            raise ValueError('Refresh token revoked.')

        if stored_token.expires_at <= datetime.datetime.now(datetime.timezone.utc):
            raise ValueError('Refresh token expired.')

        user_id = stored_token.user_id
        await self.refresh_repo.revoke(refresh_token_hash)

        access_token = self.token_service.create_access_token(user_id)
        new_refresh_token = self.token_service.create_refresh_token()
        new_refresh_hash = self.token_service.hash_refresh_token(new_refresh_token)

        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=self.token_service.refresh_token_expire_days
        )

        await self.refresh_repo.create(
            {"user_id": user_id, "token_hash": new_refresh_hash, 'expires_at': expires_at}
        )

        await self.session.commit()

        return {"access_token": access_token, "refresh_token": new_refresh_token}

    async def logout(self, refresh_token: str) -> None:
        refresh_token_hash = self.token_service.hash_refresh_token(refresh_token)
        exists = await self.refresh_repo.get_by_hash(refresh_token_hash)

        if exists is None:
            raise ValueError('Refresh token not found')

        await self.refresh_repo.revoke(refresh_token_hash)
        await self.session.commit()
