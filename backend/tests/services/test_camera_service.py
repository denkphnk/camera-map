import pytest
from redis.asyncio import Redis

from src.domain.services.camera_service import CameraService


@pytest.mark.asyncio
async def test_get_camera_by_id(
    db_session,
):
    redis = Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )

    service = CameraService(
        db_session,
        redis,
    )

    camera = await service.camera_repo.create(
        {
            "camera_id": "CAM001",
            "camera_name": "Camera Service",
            "camera_latitude": 54.7,
            "camera_longitude": 20.5,
            "archive": 0,
        }
    )

    await db_session.commit()

    found = await service.get_camera_by_id(
        camera.id
    )

    assert found is not None
    assert found.id == camera.id


@pytest.mark.asyncio
async def test_get_camera_by_id_not_found(
    db_session,
):
    redis = Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )

    service = CameraService(
        db_session,
        redis,
    )

    result = await service.get_camera_by_id(
        "11111111-1111-1111-1111-111111111111"
    )

    assert result is None