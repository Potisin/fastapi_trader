from datetime import datetime

from pydantic import BaseModel


class OperationSchema(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        orm_mode = True
