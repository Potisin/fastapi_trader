from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.models import Message
from database import async_session_maker, get_async_session

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, text: str, websocket: WebSocket):
        await websocket.send_text(text)

    async def broadcast(self, text: str, add_to_db: bool):
        if add_to_db:
            await self.add_message_to_db(text)
        for connection in self.active_connections:
            await connection.send_text(text)

    @staticmethod
    async def add_message_to_db(text: str):
        async with async_session_maker() as session:
            stmt = insert(Message).values(text=text)
            await session.scalars(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get('/last_messages')
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    query = select(Message).order_by(Message.id.desc()).limit(5)
    messages = await session.scalars(query)
    return messages.all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
