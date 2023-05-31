from fastapi import APIRouter, Depends
# from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationSchema

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


# @cache(expire=30)
@router.get("/")
async def get_specific_operations(type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Operation).where(Operation.type == type)
    result = await session.scalars(query)
    # time.sleep(3)
    data = result.all()
    return {
        'status': 'success',
        'data': data,
        'details': None
    }


@router.post('/')
async def add_specific_operations(new_operation: OperationSchema,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
