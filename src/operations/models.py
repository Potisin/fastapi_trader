from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[str]
    figi: Mapped[str]
    instrument_type: Mapped[str]
    date: Mapped[datetime]
    type: Mapped[str]
