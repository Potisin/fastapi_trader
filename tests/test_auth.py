from sqlalchemy import insert, select

from auth.models import Role
from tests.conftest import async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name='admin', permissions=None)
        await session.execute(stmt)
        await session.commit()
        query = select(Role)
        result = await session.scalar(query)
        print(result)
        print(result.id)


def test_registration():
    assert 1 == 1
