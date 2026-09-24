import pytest

from src.data.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user(
    db_session,
):
    repo = UserRepository(db_session)

    user = await repo.create(
        {
            "email": "create@test.com",
            "full_name": "Create User",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    assert user.id is not None
    assert user.email == "create@test.com"


@pytest.mark.asyncio
async def test_get_by_email(
    db_session,
):
    repo = UserRepository(db_session)

    await repo.create(
        {
            "email": "email@test.com",
            "full_name": "Email User",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    user = await repo.get_by_email(
        "email@test.com"
    )

    assert user is not None
    assert user.email == "email@test.com"


@pytest.mark.asyncio
async def test_exists_by_email(
    db_session,
):
    repo = UserRepository(db_session)

    await repo.create(
        {
            "email": "exists@test.com",
            "full_name": "Exists User",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    exists = await repo.exists_by_email(
        "exists@test.com"
    )

    assert exists is True


@pytest.mark.asyncio
async def test_get_by_id(
    db_session,
):
    repo = UserRepository(db_session)

    created_user = await repo.create(
        {
            "email": "id@test.com",
            "full_name": "Id User",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    user = await repo.get_by_id(
        created_user.id
    )

    assert user is not None
    assert user.id == created_user.id


@pytest.mark.asyncio
async def test_update_user(
    db_session,
):
    repo = UserRepository(db_session)

    user = await repo.create(
        {
            "email": "update@test.com",
            "full_name": "Old Name",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    updated_user = await repo.update(
        user.id,
        {
            "full_name": "New Name",
        },
    )

    await db_session.commit()

    assert updated_user is not None
    assert updated_user.full_name == "New Name"


@pytest.mark.asyncio
async def test_delete_user(
    db_session,
):
    repo = UserRepository(db_session)

    user = await repo.create(
        {
            "email": "delete@test.com",
            "full_name": "Delete User",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    deleted = await repo.delete(
        user.id
    )

    await db_session.commit()

    assert deleted is True

    found_user = await repo.get_by_id(
        user.id
    )

    assert found_user is None


@pytest.mark.asyncio
async def test_search_user(
    db_session,
):
    repo = UserRepository(db_session)

    await repo.create(
        {
            "email": "john@test.com",
            "full_name": "John Doe",
            "password_hash": "hash",
        }
    )

    await repo.create(
        {
            "email": "kate@test.com",
            "full_name": "Kate Smith",
            "password_hash": "hash",
        }
    )

    await db_session.commit()

    users, total = await repo.search(
        search_term="john"
    )

    assert total == 1
    assert len(users) == 1
    assert users[0].email == "john@test.com"