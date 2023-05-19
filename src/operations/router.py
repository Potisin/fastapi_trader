import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationSchema

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get("/")
@cache(expire=30)
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.execute(query)
        time.sleep(3)
        return {
            'status': 'success',
            'data': [dict(r._mapping) for r in result],
            'details': None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('/')
async def add_specific_operations(new_operation: OperationSchema,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
