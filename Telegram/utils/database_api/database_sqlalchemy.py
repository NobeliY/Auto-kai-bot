import asyncio
import logging
from datetime import datetime

from colorama import Fore

from Data import POSTGRES_URL
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

database = asyncio.get_event_loop().run_until_complete(create_async_engine)
Base = declarative_base()

class TimeDatabaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=datetime.now().strftime(""))
    updated_at = Column(
        DateTime(True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=datetime.now().strftime(""),
    )


async def create_async_database():
    engine = create_async_engine(POSTGRES_URL)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            return session


async def on_close():
    await database.close_all()
