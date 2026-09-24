import pytest

from src.data.models.analysis_model import AnalysisStatus
from src.data.models.analysis_model import Analysis
from src.data.models.user_model import User
from src.data.models.camera_model import DCamera
from src.data.models.video_model import Video
from src.data.repositories.analysis_repository import AnalysisRepository


async def create_user(db_session):
    user = User(
        email="analysis@test.com",
        full_name="Analysis User",
        password_hash="hash",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def create_camera(db_session):
    camera = DCamera(
        camera_id="CAM001",
        camera_name="Analysis Camera",
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
    suffix="1",
):
    video = Video(
        name=f"video_{suffix}",
        duration=10,
        video_resolution="1920x1080",
        fps=30,
        time_of_day="day",
        tracing="done",
        author_id=user.id,
        camera_id=camera.id,
        counter=0,
        file_object_key=f"video_{suffix}.mp4",
        file_size=100,
        content_type="video/mp4",
        preview_object_key=f"preview_{suffix}.jpg",
    )

    db_session.add(video)
    await db_session.commit()
    await db_session.refresh(video)

    return video


async def create_analysis(
    db_session,
    video,
):
    analysis = Analysis(
        video_id=video.id,
    )

    db_session.add(analysis)
    await db_session.commit()
    await db_session.refresh(analysis)

    return analysis


@pytest.mark.asyncio
async def test_get_by_video_id(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await create_analysis(
        db_session,
        video,
    )

    found = await repo.get_by_video_id(
        video.id,
    )

    assert found is not None
    assert found.id == analysis.id


@pytest.mark.asyncio
async def test_get_by_video_id_not_found(db_session):
    repo = AnalysisRepository(db_session)

    result = await repo.get_by_video_id(
        "11111111-1111-1111-1111-111111111111"
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_all(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    video1 = await create_video(
        db_session,
        user,
        camera,
        "1",
    )

    video2 = await create_video(
        db_session,
        user,
        camera,
        "2",
    )

    await create_analysis(db_session, video1)
    await create_analysis(db_session, video2)

    result = await repo.get_all()

    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_all_by_status(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    video = await create_video(
        db_session,
        user,
        camera,
    )

    analysis = await create_analysis(
        db_session,
        video,
    )

    await repo.set_processing(analysis.id)
    await db_session.commit()

    result = await repo.get_all(
        status=AnalysisStatus.PROCESSING,
    )

    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_all_by_video_id(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    video = await create_video(
        db_session,
        user,
        camera,
    )

    await create_analysis(
        db_session,
        video,
    )

    result = await repo.get_all(
        video_id=video.id,
    )

    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_all_by_camera_id(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)

    video = await create_video(
        db_session,
        user,
        camera,
    )

    await create_analysis(
        db_session,
        video,
    )

    result = await repo.get_all(
        camera_id=camera.id,
    )

    assert len(result) == 1


@pytest.mark.asyncio
async def test_set_processing(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await create_analysis(
        db_session,
        video,
    )

    updated = await repo.set_processing(
        analysis.id,
    )

    await db_session.commit()

    assert updated is not None
    assert updated.status == AnalysisStatus.PROCESSING
    assert updated.started_at is not None


@pytest.mark.asyncio
async def test_set_done(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await create_analysis(
        db_session,
        video,
    )

    updated = await repo.set_done(
        analysis.id,
        {
            "cars": 10,
        },
    )

    await db_session.commit()

    assert updated is not None
    assert updated.status == AnalysisStatus.DONE
    assert updated.result == {"cars": 10}
    assert updated.finished_at is not None


@pytest.mark.asyncio
async def test_set_error(db_session):
    repo = AnalysisRepository(db_session)

    user = await create_user(db_session)
    camera = await create_camera(db_session)
    video = await create_video(db_session, user, camera)

    analysis = await create_analysis(
        db_session,
        video,
    )

    updated = await repo.set_error(
        analysis.id,
        "something went wrong",
    )

    await db_session.commit()

    assert updated is not None
    assert updated.status == AnalysisStatus.ERROR
    assert updated.error_message == "something went wrong"
    assert updated.finished_at is not None