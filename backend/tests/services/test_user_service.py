import pytest

from src.domain.services.user_service import UserService
from src.domain.schemas.user_schemas import UserUpdateRequest
from src.data.models.user_model import User
from src.data.models.camera_model import DCamera
from src.data.models.video_model import Video


async def create_user(db_session):
    user = User(
        email="test@test.com",
        full_name="Test User",
        password_hash="hash",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def create_camera(db_session):
    camera = DCamera(
        camera_id="CAM001",
        camera_name="Test Camera",
        camera_latitude=54.7,
        camera_longitude=20.5,
        archive=0,
    )

    db_session.add(camera)
    await db_session.commit()
    await db_session.refresh(camera)

    return camera


async def create_video(
    db_session,
    user,
    camera,
):
    video = Video(
        name="test_video",
        time_of_day="day",
        tracing="done",
        author_id=user.id,
        camera_id=camera.id,
        counter=0,
        file_object_key=f"video_{user.id}.mp4",
        file_size=100,
        content_type="video/mp4",
        preview_object_key=f"preview_{user.id}.jpg",
    )

    db_session.add(video)
    await db_session.commit()
    await db_session.refresh(video)

    return video


@pytest.mark.asyncio
async def test_get_me(
    db_session,
):
    service = UserService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    await create_video(
        db_session,
        user,
        camera,
    )

    profile = await service.get_me(user.id)

    assert profile is not None
    assert profile.id == user.id
    assert profile.email == user.email
    assert profile.full_name == user.full_name
    assert profile.total_videos == 1
    assert len(profile.videos) == 1


@pytest.mark.asyncio
async def test_get_me_not_found(
    db_session,
):
    service = UserService(db_session)

    profile = await service.get_me(
        "11111111-1111-1111-1111-111111111111"
    )

    assert profile is None


@pytest.mark.asyncio
async def test_update_me_full_name(
    db_session,
):
    service = UserService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    await create_video(
        db_session,
        user,
        camera,
    )

    result = await service.update_me(
        user.id,
        UserUpdateRequest(
            full_name="Updated User",
        ),
    )

    assert result is not None
    assert result.full_name == "Updated User"
    assert result.email == user.email
    assert result.total_videos == 1


@pytest.mark.asyncio
async def test_update_me_not_found(
    db_session,
):
    service = UserService(db_session)

    result = await service.update_me(
        "11111111-1111-1111-1111-111111111111",
        UserUpdateRequest(
            full_name="New Name",
        ),
    )

    assert result is None


@pytest.mark.asyncio
async def test_update_me_empty_payload(
    db_session,
):
    service = UserService(db_session)

    user = await create_user(db_session)

    with pytest.raises(
        ValueError,
        match="No fields to update",
    ):
        await service.update_me(
            user.id,
            UserUpdateRequest(),
        )