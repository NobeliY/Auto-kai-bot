from sqlalchemy import select, delete, ForeignKey, Column, BigInteger, String, Integer, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert, JSON
from sqlalchemy.orm import relationship

from utils.database_api.database_gino import TimeDatabaseModel, database, BaseModel


class User(TimeDatabaseModel):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, unique=True)
    initials = Column(String, primary_key=True, unique=True)
    email = Column(String)
    phoneNumber = Column(String)
    group = Column(String)
    stateNumber = Column(String)
    access = Column(String, primary_key=True)

    query: select
    foreigns = [
        relationship("ApplicationChange", cascade="all,delete"),
        relationship("DateQuality", cascade="all,delete"),
        relationship("ParkingLog", cascade="all,delete")
    ]


class Application(TimeDatabaseModel):
    __tablename__ = "applications"
    id = Column(BigInteger, primary_key=True, unique=True)
    initials = Column(String, primary_key=True)
    email = Column(String, primary_key=True)
    phoneNumber = Column(String, primary_key=True)
    group = Column(String, primary_key=True)
    stateNumber = Column(String, primary_key=True)

    query: select


class ApplicationChange(TimeDatabaseModel):
    __tablename__ = "application_changes"
    id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
                primary_key=True)
    initials = Column(String, primary_key=True)
    email = Column(String, primary_key=True)
    phoneNumber = Column(String, primary_key=True)
    group = Column(String, primary_key=True)
    stateNumber = Column(String, primary_key=True)

    query: select


class DateQuality(BaseModel):
    __tablename__ = "date_quality"
    id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
                primary_key=True)
    times = Column(String, primary_key=True)
    count = Column(Integer, primary_key=True)

    query: select


class ParkingLog(TimeDatabaseModel):
    __tablename__ = "parking_logs"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    time_from_user = Column(String)
    initials = Column(String, ForeignKey("users.initials", ondelete="CASCADE"))

    query: select
    add: insert


class AiogramState(BaseModel):
    __tablename__ = "aiogram_states"

    user = Column(BigInteger, nullable=False, primary_key=True)
    chat = Column(BigInteger, nullable=False)
    state = Column(String, nullable=False)

    query: select
    add: insert


class AiogramData(BaseModel):
    __tablename__ = "aiogram_datas"
    user = Column(BigInteger, nullable=False, primary_key=True)
    chat = Column(BigInteger, nullable=False)
    data = Column(JSON, nullable=True)

    query: select
    add: insert


class AiogramBucket(BaseModel):
    __tablename__ = "aiogram_buckets"
    user = Column(BigInteger, nullable=False, primary_key=True)
    chat = Column(BigInteger, nullable=False)
    bucket = Column(JSON, nullable=False)

    query: select
    add: insert
