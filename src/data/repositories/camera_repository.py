from sqlalchemy import select

from src.data.models.camera_model import DCamera
from src.data.repositories.base_repository import BaseRepository


class CameraRepository(BaseRepository[DCamera]):
    async def get_by_camera_id(self, camera_id: str) -> DCamera | None:
        query = select(self.model).where(self.model.camera_id == camera_id)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()