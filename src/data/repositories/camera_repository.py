from sqlalchemy import select

from src.data.models.camera_model import DCamera
from src.data.repositories.base_repository import BaseRepository
from src.domain.schemas.camera_schemas import CameraSearchFilters

class CameraRepository(BaseRepository[DCamera]):
    async def get_by_camera_id(self, camera_id: str) -> DCamera | None:
        query = select(self.model).where(self.model.camera_id == camera_id)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def search(self, filters: CameraSearchFilters) -> list[DCamera]:
        query = select(self.model)
        conditions = []
        
        # Полнотекстовый поиск по названию
        if filters.search:
            conditions.append(self.model.camera_name.ilike(f"%{filters.search}%"))
        
        # Точные совпадения
        if filters.model:
            conditions.append(self.model.model == filters.model)
        if filters.camera_type:
            conditions.append(self.model.camera_type == filters.camera_type)
        if filters.camera_class:
            conditions.append(self.model.camera_class == filters.camera_class)
        
        if conditions:
            query = query.where(*conditions)
        
        result = await self.session.execute(query)
        return result.scalars().all()
        