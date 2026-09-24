import pytest

from src.domain.services.analysis_service import AnalysisService
from src.domain.schemas.analysis_schemas import AnalysisFilters
from src.data.models.analysis_model import AnalysisStatus
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
async def test_get_by_id(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await service.create(video.id)

    found = await service.get_by_id(analysis.id)

    assert found is not None
    assert found.id == analysis.id


@pytest.mark.asyncio
async def test_get_by_video_id(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await service.create(video.id)

    found = await service.get_by_video_id(video.id)

    assert found is not None
    assert found.id == analysis.id


@pytest.mark.asyncio
async def test_create_analysis(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await service.create(video.id)

    assert analysis.video_id == video.id


@pytest.mark.asyncio
async def test_create_analysis_video_not_found(
    db_session,
):
    service = AnalysisService(db_session)

    with pytest.raises(ValueError, match="Video not found"):
        await service.create(
            "11111111-1111-1111-1111-111111111111"
        )


@pytest.mark.asyncio
async def test_create_analysis_already_exists(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    await service.create(video.id)

    with pytest.raises(ValueError, match="Analysis already exists"):
        await service.create(video.id)


@pytest.mark.asyncio
async def test_start_analysis(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await service.create(video.id)

    await service.start_analysis(analysis.id)

    updated = await service.get_by_id(analysis.id)

    assert updated.status == AnalysisStatus.PROCESSING


@pytest.mark.asyncio
async def test_start_analysis_not_found(
    db_session,
):
    service = AnalysisService(db_session)

    with pytest.raises(ValueError, match="Analysis not found"):
        await service.start_analysis(
            "11111111-1111-1111-1111-111111111111"
        )


@pytest.mark.asyncio
async def test_finish_analysis(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await service.create(video.id)

    result = {
        "tracks": [],
        "objects_count": 10,
    }

    await service.finish_analysis(
        analysis.id,
        result,
    )

    updated = await service.get_by_id(analysis.id)

    assert updated.status == AnalysisStatus.DONE
    assert updated.result == result


@pytest.mark.asyncio
async def test_finish_analysis_not_found(
    db_session,
):
    service = AnalysisService(db_session)

    with pytest.raises(ValueError, match="Analysis not found"):
        await service.finish_analysis(
            "11111111-1111-1111-1111-111111111111",
            {},
        )


@pytest.mark.asyncio
async def test_fail_analysis(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await service.create(video.id)

    await service.fail_analysis(
        analysis.id,
        "Test error",
    )

    updated = await service.get_by_id(analysis.id)

    assert updated.status == AnalysisStatus.ERROR
    assert updated.error_message == "Test error"


@pytest.mark.asyncio
async def test_fail_analysis_not_found(
    db_session,
):
    service = AnalysisService(db_session)

    with pytest.raises(ValueError, match="Analysis not found"):
        await service.fail_analysis(
            "11111111-1111-1111-1111-111111111111",
            "error",
        )


@pytest.mark.asyncio
async def test_get_all(
    db_session,
):
    service = AnalysisService(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    await service.create(video.id)

    result = await service.get_all(
        AnalysisFilters(),
    )

    assert len(result) == 1
    assert result[0].video_name == video.name
    assert result[0].camera_name == camera.camera_name