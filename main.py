from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title='Trader App')

fake_trades = [
    {'id': 1, "user_id": 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.21},
    {'id': 2, "user_id": 1, 'currency': 'BTC', 'side': 'buy', 'price': 456, 'amount': 2.31}
]

fake_users = [
    {'id': 1, 'username': 'shji9pa', 'name': 'maks'},
    {'id': 2, 'username': 'potisin', 'name': 'maksim'},
    {'id': 3, 'username': 'nnnas', 'name': 'maksimnnn', 'degree': [
        {'id': '1', 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}
    ]},
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=6)
    side: str
    price: float = Field(ge=0)
    amount: float


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType # только указанные типы класса DegreeType


class User(BaseModel):
    id: int
    username: str
    name: str
    degree: Optional[List[Degree]] = []  # необязательное поле, возвращает список (типа как кверисет) модели Degree.
    # Если кверисет пустой, то возвращает список


@app.get('/users/{user_id}/', response_model=List[User])
def first(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


@app.get('/users/')
def second(user_id: int = 0):
    print(isinstance(user_id, str))
    print(isinstance(user_id, int))
    return user_id


@app.post('/trades')
def add_trades(trades: List[Trade]):
    # fake_trades.extend(trades)  # Пичарм ругается на несоответствие типов trades
    fake_trades.extend([dict(trade) for trade in trades])  # рекомендация CG
    return {'status': 200, 'data': fake_trades}
