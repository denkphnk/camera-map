from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.schemas.user_schemas import UserUpdateRequest, UserProfileResponse
from src.data.repositories.user_repository import UserRepository
from src.data.repositories.video_repository import VideoRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.video_repo = VideoRepository(session)


    async def get_me(self, user_id: UUID) -> UserProfileResponse | None:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            return None
        
        videos, total = await self.video_repo.get_by_author(user_id)

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            videos=videos,
            total_videos=total
        )

    async def update_me(self, user_id: UUID, data: UserUpdateRequest) -> UserProfileResponse | None:
        if not data.model_dump(exclude_unset=True):
            raise ValueError('No fields to update')
        
        user = await self.user_repo.update(user_id, data.model_dump(exclude_unset=True))
        if user is None:
            return None

        await self.session.commit()
        await self.session.refresh(user)

        videos, total = await self.video_repo.get_by_author(user_id)

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            videos=videos,
            total_videos=total
        )