from datetime import datetime, timezone

from sqlalchemy import select, update

from src.data.repositories.base_repository import BaseRepository
from src.data.models.refresh_token_model import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Класс для работы с RefreshTokens"""
    def __init__(self, session):
        super().__init__(RefreshToken, session)

    ##########################################
    # ПОИСК ПО TOKEN_HASH
    ##########################################
    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        query = select(self.model).where(self.model.token_hash == token_hash)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    ##########################################
    # REVOKE
    ##########################################
    async def revoke(self, token_hash: str) -> RefreshToken | None:
        query = (
            update(self.model)
            .where(self.model.token_hash == token_hash)
            .values(revoked_at=datetime.now(timezone.utc))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        await self.session.flush()

        return result.scalar_one_or_none()
