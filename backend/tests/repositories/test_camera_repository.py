import uuid

import pytest

from src.data.models.camera_model import DCamera
from src.data.models.user_model import User
from src.data.models.video_model import Video
from src.data.repositories.camera_repository import CameraRepository
from src.domain.schemas.camera_schemas import CameraSearchFilters


@pytest.mark.asyncio
async def test_get_by_camera_id(
    db_session,
):
    repo = CameraRepository(db_session)

    camera = await repo.create(
        {
            "camera_id": "CAM001",
            "camera_name": "Test Camera",
            "camera_latitude": 54.7,
            "camera_longitude": 20.5,
            "archive": 0,
        }
    )

    await db_session.commit()

    found = await repo.get_by_camera_id(
        "CAM001"
    )

    assert found is not None
    assert found.id == camera.id


@pytest.mark.asyncio
async def test_get_cameras_with_video_count(
    db_session,
):
    camera_repo = CameraRepository(db_session)

    camera = await camera_repo.create(
        {
            "camera_id": "CAM002",
            "camera_name": "Camera With Video",
            "camera_latitude": 54.7,
            "camera_longitude": 20.5,
            "archive": 0,
        }
    )

    user = User(
        email="camera@test.com",
        full_name="Camera User",
        password_hash="hash",
    )

    db_session.add(user)
    await db_session.flush()

    video = Video(
        name="video.mp4",
        time_of_day="day",
        tracing="done",
        author_id=user.id,
        camera_id=camera.id,
        file_object_key=f"{uuid.uuid4()}.mp4",
        file_size=100,
        content_type="video/mp4",
    )

    db_session.add(video)

    await db_session.commit()

    result = await camera_repo.get_cameras_with_video_count()

    camera_row, video_count = result[0]

    assert camera_row.id == camera.id
    assert video_count == 1


@pytest.mark.asyncio
async def test_search_camera_by_name(
    db_session,
):
    repo = CameraRepository(db_session)

    await repo.create(
        {
            "camera_id": "CAM003",
            "camera_name": "Speed Camera",
            "camera_latitude": 54.7,
            "camera_longitude": 20.5,
            "archive": 0,
        }
    )

    await repo.create(
        {
            "camera_id": "CAM004",
            "camera_name": "Traffic Camera",
            "camera_latitude": 54.7,
            "camera_longitude": 20.5,
            "archive": 0,
        }
    )

    await db_session.commit()

    filters = CameraSearchFilters(
        search="Speed",
        model=None,
        camera_type=None,
        camera_class=None,
        video_count_from=None,
        video_count_to=None,
    )

    result = await repo.search(filters)

    assert len(result) == 1

    camera, _ = result[0]

    assert camera.camera_name == "Speed Camera"