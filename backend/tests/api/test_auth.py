import pytest


@pytest.mark.asyncio
async def test_register_success(
    client,
):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "register@test.com",
            "full_name": "Register User",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "register@test.com"
    assert data["full_name"] == "Register User"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(
    client,
):
    payload = {
        "email": "duplicate@test.com",
        "full_name": "Duplicate User",
        "password": "password123",
    }

    await client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    response = await client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code >= 400


@pytest.mark.asyncio
async def test_login_success(
    client,
):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@test.com",
            "full_name": "Login User",
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(
    client,
):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong@test.com",
            "full_name": "Wrong Password User",
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@test.com",
            "password": "bad_password",
        },
    )

    assert response.status_code >= 400


@pytest.mark.asyncio
async def test_login_user_not_found(
    client,
):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "missing@test.com",
            "password": "password123",
        },
    )

    assert response.status_code >= 400


@pytest.mark.asyncio
async def test_refresh_success(
    client,
):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh@test.com",
            "full_name": "Refresh User",
            "password": "password123",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh@test.com",
            "password": "password123",
        },
    )

    refresh_token = login_response.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_invalid_token(
    client,
):
    response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid_token",
        },
    )

    assert response.status_code >= 400


@pytest.mark.asyncio
async def test_logout_success(
    client,
):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "logout@test.com",
            "full_name": "Logout User",
            "password": "password123",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "logout@test.com",
            "password": "password123",
        },
    )

    refresh_token = login_response.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_logout_invalid_token(
    client,
):
    response = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": "invalid_token",
        },
    )

    assert response.status_code >= 400