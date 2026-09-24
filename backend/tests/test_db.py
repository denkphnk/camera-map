import pytest

from sqlalchemy import text


@pytest.mark.asyncio
async def test_database_connection(
    db_session,
):
    result = await db_session.execute(
        text("SELECT 1")
    )

    assert result.scalar() == 1