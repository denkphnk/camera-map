import uuid

import pytest

from src.data.models.camera_model import DCamera


@pytest.mark.asyncio
async def test_get_camera_by_id(
    client,
    db_session,
):
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

    response = await client.get(
        f"/api/v1/cameras/{camera.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(camera.id)
    assert data["camera_id"] == "CAM001"
    assert data["camera_name"] == "Test Camera"


@pytest.mark.asyncio
async def test_get_camera_by_id_not_found(
    client,
):
    response = await client.get(
        f"/api/v1/cameras/{uuid.uuid4()}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_cameras(
    client,
    db_session,
):
    camera = DCamera(
        camera_id="CAM123",
        camera_name="Search Camera",
        camera_place="Test Place",
        camera_latitude=54.7,
        camera_longitude=20.5,
        archive=0,
    )

    db_session.add(camera)
    await db_session.commit()

    response = await client.get(
        "/api/v1/cameras/",
        params={
            "search": "Search",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["camera_name"] == "Search Camera"


@pytest.mark.asyncio
async def test_search_cameras_empty_result(
    client,
):
    response = await client.get(
        "/api/v1/cameras/",
        params={
            "search": "NOT_EXISTING_CAMERA",
        },
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_geojson(
    client,
    db_session,
):
    camera = DCamera(
        camera_id="CAM999",
        camera_name="Geo Camera",
        camera_place="Geo Place",
        camera_latitude=54.7,
        camera_longitude=20.5,
        archive=0,
    )

    db_session.add(camera)
    await db_session.commit()

    response = await client.get(
        "/api/v1/cameras/geojson"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1

    feature = data["features"][0]

    assert feature["properties"]["camera_id"] == "CAM999"
    assert feature["properties"]["camera_name"] == "Geo Camera"


@pytest.mark.asyncio
async def test_get_camera_details_not_found(
    client,
):
    response = await client.get(
        f"/api/v1/cameras/{uuid.uuid4()}/details"
    )

    assert response.status_code == 404