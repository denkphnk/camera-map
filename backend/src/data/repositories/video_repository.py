from typing import Any

from sqlalchemy import func, select, update

from src.data.models.video_model import Video
from src.data.repositories.base_repository import BaseRepository


class VideoRepository(BaseRepository[Video]):
    """Класс для работы с Video"""

    def __init__(self, session):
        super().__init__(Video, session)

    async def get_by_author(
        self, author_id: Any, offset: int = 0, limit: int = 20
    ) -> tuple[list[Video], int]:
        videos = (
            select(self.model)
            .where(self.model.author_id == author_id)
            .order_by(self.model.created_at.desc())
        )
        total = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.author_id == author_id)
        )

        videos = videos.offset(offset).limit(limit)

        result = await self.session.execute(videos)
        result_total = await self.session.execute(total)
        return result.scalars().all(), result_total.scalar_one()

    async def get_by_camera(
        self, camera_id: Any, offset: int = 0, limit: int = 20
    ) -> tuple[list[Video], int]:
        videos = (
            select(self.model)
            .where(self.model.camera_id == camera_id)
            .order_by(self.model.created_at.desc() )
        )
        total = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.camera_id == camera_id)
        )

        videos = videos.offset(offset).limit(limit)

        result = await self.session.execute(videos)
        result_total = await self.session.execute(total)
        return result.scalars().all(), result_total.scalar_one()

    async def search(
        self,
        name: str | None = None,
        author_id: Any | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Video], int]:
        videos = select(self.model)
        total = select(func.count()).select_from(self.model)

        if name and name.strip():
            name = f"%{name}%"
            videos = videos.where(self.model.name.ilike(name))
            total = total.where(self.model.name.ilike(name))

        if author_id:
            videos = videos.where(self.model.author_id == author_id)
            total = total.where(self.model.author_id == author_id)

        videos = (
            videos.offset(offset).limit(limit).order_by(self.model.created_at.desc())
        )

        result = await self.session.execute(videos)
        result_total = await self.session.execute(total)

        return result.scalars().all(), result_total.scalar_one()

    async def increment_counter(self, video_id: Any) -> Video | None:
        query = (
            update(self.model)
            .where(self.model.id == video_id)
            .values(counter=self.model.counter + 1)
            .returning(self.model)
        )

        video = await self.session.execute(query)
        return video.scalar_one_or_none()
