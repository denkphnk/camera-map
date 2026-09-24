import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from src.main import app
from src.core.database import Base, get_db


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/camera_map_test"
)
import pytest_asyncio


from src.core.cache import get_redis

class FakeRedis:
    async def get(self, *args, **kwargs):
        return None

    async def set(self, *args, **kwargs):
        return True


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture
async def db_session(session_factory):
    async with session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
async def prepare_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[
        get_db
    ] = override_get_db
    app.dependency_overrides[get_redis] = lambda: FakeRedis()

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()