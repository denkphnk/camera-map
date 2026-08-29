from sqlalchemy import func, or_, select

from src.data.repositories.base_repository import BaseRepository
from src.data.models.user_model import User


class UserRepository(BaseRepository[User]):
    """Класс для работы с Users"""

    ##########################################
    # ПОИСК ПО EMAIL
    ##########################################
    async def get_by_email(self, email: str) -> User | None:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        return await self.exists(email=email)

    ##########################################
    # ПОИСК
    ##########################################
    async def search(
        self, search_term: str | None, offset: int = 0, limit: int = 20
    ) -> tuple[list[User], int]:
        query = select(self.model)
        total_query = select(func.count()).select_from(self.model)
        if search_term and search_term.strip():
            search_term = f"%{search_term}%"
            search_filter = or_(
                self.model.email.ilike(search_term),
                self.model.full_name.ilike(search_term),
            )
            query = query.where(search_filter)

            total_query = total_query.where(search_filter)

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        total = await self.session.execute(total_query)

        return result.scalars().all(), total.scalar_one()
