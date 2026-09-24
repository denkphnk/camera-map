import pytest

from src.data.models.camera_model import DCamera
from src.data.models.user_model import User
from src.data.models.video_model import Video
from src.data.repositories.video_repository import VideoRepository


async def create_user(db_session):
    user = User(
        email="video@test.com",
        full_name="Video User",
        password_hash="hash",
    )

    db_session.add(user)
    await db_session.commit()

    return user


async def create_camera(db_session):
    camera = DCamera(
        camera_id="CAM001",
        camera_name="Test Camera",
        camera_place="Test Place",
        camera_latitude=54.7,
        camera_longitude=20.5,
        archive=0,
    )

    db_session.add(camera)
    await db_session.commit()

    return camera


async def create_video(
    db_session,
    user,
    camera,
    name="test_video",
    tracing="done",
):
    video = Video(
        name=name,
        time_of_day="day",
        tracing=tracing,
        author_id=user.id,
        camera_id=camera.id,
        file_object_key=f"{name}.mp4",
        file_size=100,
        content_type="video/mp4",
    )

    db_session.add(video)
    await db_session.commit()

    return video


@pytest.mark.asyncio
async def test_get_by_author(
    db_session,
):
    repo = VideoRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    await create_video(db_session, user, camera)

    videos, total = await repo.get_by_author(user.id)

    assert total == 1
    assert len(videos) == 1
    assert videos[0].author_id == user.id


@pytest.mark.asyncio
async def test_get_by_camera(
    db_session,
):
    repo = VideoRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    await create_video(db_session, user, camera)

    videos, total = await repo.get_by_camera(camera.id)

    assert total == 1
    assert len(videos) == 1
    assert videos[0].camera_id == camera.id


@pytest.mark.asyncio
async def test_search_video_by_name(
    db_session,
):
    repo = VideoRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    await create_video(
        db_session,
        user,
        camera,
        name="search_video",
    )

    videos, total = await repo.search(
        name="search"
    )

    assert total == 1
    assert len(videos) == 1
    assert videos[0].name == "search_video"


@pytest.mark.asyncio
async def test_increment_counter(
    db_session,
):
    repo = VideoRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    video = await create_video(
        db_session,
        user,
        camera,
    )

    updated_video = await repo.increment_counter(
        video.id
    )

    await db_session.commit()

    assert updated_video is not None
    assert updated_video.counter == 1


@pytest.mark.asyncio
async def test_exists_processing_video(
    db_session,
):
    repo = VideoRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    processing_video = await create_video(
        db_session,
        user,
        camera,
        tracing="processing",
        name='test_video1'
    )

    another_video = await create_video(
        db_session,
        user,
        camera,
        tracing="done",
    )

    exists = await repo.exists_processing_video(
        author_id=user.id,
        exclude_video_id=another_video.id,
    )

    assert exists is True


@pytest.mark.asyncio
async def test_get_next_queued_video(
    db_session,
):
    repo = VideoRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    queued_video = await create_video(
        db_session,
        user,
        camera,
        tracing="queued",
    )

    result = await repo.get_next_queued_video(
        user.id
    )

    assert result is not None
    assert result.id == queued_video.id