from typing import Any

from sqlalchemy import func, select, update

from src.data.models.video_model import Video
from src.data.models.user_model import User
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
    ):
        query = (
            select(
                Video,
                User.full_name.label("author_name"),
            )
            .join(
                User,
                User.id == Video.author_id,
            )
        )

        total_query = select(
            func.count()
        ).select_from(Video)

        if name and name.strip():
            pattern = f"%{name}%"

            query = query.where(
                Video.name.ilike(pattern)
            )

            total_query = total_query.where(
                Video.name.ilike(pattern)
            )

        if author_id:
            query = query.where(
                Video.author_id == author_id
            )

            total_query = total_query.where(
                Video.author_id == author_id
            )

        query = (
            query
            .order_by(Video.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(
            query
        )

        total_result = (
            await self.session.execute(
                total_query
            )
        )

        videos = []

        for video, author_name in result.all():
            video.author_name = author_name
            videos.append(video)

        return (
            videos,
            total_result.scalar_one(),
        )
    
    async def increment_counter(self, video_id: Any) -> Video | None:
        query = (
            update(self.model)
            .where(self.model.id == video_id)
            .values(counter=self.model.counter + 1)
            .returning(self.model)
        )

        video = await self.session.execute(query)
        return video.scalar_one_or_none()

    async def exists_processing_video(
        self,
        author_id: Any,
        exclude_video_id: Any,
    ) -> bool:
        query = (
            select(self.model)
            .where(
                self.model.author_id == author_id,
                self.model.tracing == 'processing',
                self.model.id != exclude_video_id
            )
            .order_by(self.model.created_at.desc())
            .limit(1)
        )

        video = await self.session.execute(query)
        return bool(video.scalar_one_or_none())

    async def get_next_queued_video(
        self,
        author_id,
    ) -> Video | None:
        query = (
            select(self.model)
            .where(
                self.model.author_id == author_id,
                self.model.tracing == 'queued'
            )
            .order_by(self.model.created_at.asc())
            .limit(1)
        )

        video = await self.session.execute(query)
        return video.scalar_one_or_none()