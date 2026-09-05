import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.camera.camera_schemas import CameraResponse, CameraSearchFilters
from src.api.v1.dependencies import get_camera_service
from src.domain.services.camera_service import CameraService

camera_router = APIRouter(prefix='/cameras', tags=['Camera'])

@camera_router.get('/', response_model=list[CameraResponse])
async def get_cameras_with_filters(filters: CameraSearchFilters = Depends(), service: CameraService = Depends(get_camera_service)):
    cameras = await service.search_cameras(filters)
    return cameras

@camera_router.get('/geojson')
async def get_camera_geojson(service: CameraService = Depends(get_camera_service)):
    geojson = await service.get_geojson()
    return geojson

@camera_router.get('/{camera_id}', response_model=CameraResponse)
async def get_camera_by_id(camera_id: uuid.UUID, service: CameraService = Depends(get_camera_service)):
    camera = await service.get_camera_by_id(camera_id)
    if camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Camera not found')
    return camera
