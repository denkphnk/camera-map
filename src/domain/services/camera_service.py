import json
import logging

from uuid import UUID
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.camera_model import DCamera
from src.data.repositories.camera_repository import CameraRepository
from src.domain.schemas.camera_schemas import CameraSearchFilters

logger = logging.getLogger(__name__)

class CameraService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.camera_repo = CameraRepository(session)
        self.redis = redis

    async def get_geojson(self) -> dict:
        try:
            cached = await self.redis.get('cameras:geojson')
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Redis read failed for geojson cache: {e}")

        cameras = await self.camera_repo.get_all()

        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"camera_id": camera.camera_id, "has_video": False},
                    "geometry": {"type": "Point", "coordinates": [camera.camera_longitude, camera.camera_latitude]}
                }
            for camera in cameras]
        }

        try:
            await self.redis.set('cameras:geojson', json.dumps(geojson, default=str), ex=300)
        except Exception as e:
            logger.warning(f"Redis write failed for geojson cache: {e}")

        return geojson

    async def search_cameras(self, filters: CameraSearchFilters) -> list[DCamera]:
        if filters.search and not filters.search.strip():
            filters.search = None
        
        cameras = await self.camera_repo.search(filters)
        return cameras

    async def get_camera_by_id(self, camera_id: UUID) -> DCamera | None:
        camera = await self.camera_repo.get_by_id(camera_id)

        return camera

    async def invalidate_geojson_cache(self):
        try:
            await self.redis.delete('cameras:geojson')
        except Exception:
            logger.warning("Failed to invalidate geojson cache. Will refresh by TTL.")
            pass