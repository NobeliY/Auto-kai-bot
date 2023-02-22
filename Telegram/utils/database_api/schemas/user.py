from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select
from utils.database_api.database_gino import TimeDatabaseModel


class User(TimeDatabaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    initials = Column(String, primary_key=True)
    email = Column(String)
    phoneNumber = Column(String)
    group = Column(String)
    stateNumber = Column(String)
    access = Column(String, primary_key=True)

    query: select
    foreigns = relationship("users", cascade="all, delete")
