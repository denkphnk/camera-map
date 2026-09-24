import pytest
from redis.asyncio import Redis

from src.domain.services.videos_service import VideoService
from src.storage.minio_service import MinioService


async def create_user(service):
    return await service.user_repo.create(
        {
            "email": "user@test.com",
            "full_name": "Test User",
            "password_hash": "hash",
        }
    )


async def create_camera(service):
    return await service.camera_repo.create(
        {
            "camera_id": "CAM001",
            "camera_name": "Camera",
            "camera_latitude": 54.7,
            "camera_longitude": 20.5,
            "archive": 0,
        }
    )


async def create_video(service, user, camera, suffix="1"):
    return await service.video_repo.create(
        {
            "name": f"video_{suffix}",
            "duration": 10,
            "video_resolution": "1920x1080",
            "fps": 30,
            "time_of_day": "day",
            "tracing": "done",
            "author_id": user.id,
            "camera_id": camera.id,
            "counter": 0,
            "file_object_key": f"file_{suffix}.mp4",
            "file_size": 100,
            "content_type": "video/mp4",
            "preview_object_key": f"preview_{suffix}.jpg",
        }
    )


@pytest.fixture
def redis_client():
    return Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )


@pytest.mark.asyncio
async def test_get_video_by_id(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    user = await create_user(service)
    camera = await create_camera(service)
    video = await create_video(service, user, camera)

    await db_session.commit()

    result = await service.get_video_by_id(video.id)

    assert result is not None
    assert result.id == video.id


@pytest.mark.asyncio
async def test_get_video_by_id_not_found(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    result = await service.get_video_by_id(
        "11111111-1111-1111-1111-111111111111"
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_videos_by_author(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    user = await create_user(service)
    camera = await create_camera(service)

    await create_video(service, user, camera, "1")
    await create_video(service, user, camera, "2")

    await db_session.commit()

    videos, total = await service.get_videos_by_author(user.id)

    assert total == 2
    assert len(videos) == 2


@pytest.mark.asyncio
async def test_get_videos_by_camera(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    user = await create_user(service)
    camera = await create_camera(service)

    await create_video(service, user, camera, "1")
    await create_video(service, user, camera, "2")

    await db_session.commit()

    videos, total = await service.get_videos_by_camera(camera.id)

    assert total == 2
    assert len(videos) == 2


@pytest.mark.asyncio
async def test_search_videos(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    user = await create_user(service)
    camera = await create_camera(service)

    await create_video(service, user, camera, "search_me")
    await create_video(service, user, camera, "another")

    await db_session.commit()

    videos, total = await service.search_videos(
        name="search"
    )

    assert total == 1
    assert len(videos) == 1


@pytest.mark.asyncio
async def test_increment_counter(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    user = await create_user(service)
    camera = await create_camera(service)

    video = await create_video(
        service,
        user,
        camera,
    )

    await db_session.commit()

    updated = await service.increment_counter(video.id)

    assert updated is not None
    assert updated.counter == 1


@pytest.mark.asyncio
async def test_get_video_details(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    user = await create_user(service)
    camera = await create_camera(service)

    video = await create_video(
        service,
        user,
        camera,
    )

    await db_session.commit()

    details = await service.get_video_details(
        video.id
    )

    assert details is not None
    assert str(video.id) in details.video_url
    assert str(video.id) in details.preview_url


@pytest.mark.asyncio
async def test_get_video_details_not_found(
    db_session,
    redis_client,
):
    service = VideoService(
        db_session,
        MinioService(),
        redis_client,
    )

    result = await service.get_video_details(
        "11111111-1111-1111-1111-111111111111"
    )

    assert result is None


@pytest.mark.parametrize(
    ("hour", "expected"),
    [
        (0, "night"),
        (5, "night"),
        (6, "morning"),
        (11, "morning"),
        (12, "day"),
        (17, "day"),
        (18, "evening"),
        (23, "evening"),
    ],
)
def test_get_time_of_day(
    hour,
    expected,
):
    service = VideoService.__new__(VideoService)

    assert service._get_time_of_day(hour) == expected


@pytest.mark.parametrize(
    "hour",
    [
        -1,
        24,
    ],
)
def test_get_time_of_day_invalid(hour):
    service = VideoService.__new__(VideoService)

    with pytest.raises(ValueError):
        service._get_time_of_day(hour)