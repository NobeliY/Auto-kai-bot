from datetime import datetime
from Data import POSTGRES_URL
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine(POSTGRES_URL)
session = Session(engine)

class Base(DeclarativeBase):
    __abstract__ = True

    def __repr__(self):
        pass


class TimeDatabaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=datetime.now().strftime(""))
    updated_at = Column(
        DateTime(True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=datetime.now().strftime(""),
    )
