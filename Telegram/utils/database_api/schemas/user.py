from sqlalchemy import BigInteger, Column, String, sql
from sqlalchemy.orm import relationship
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

    query: sql.select
    foreigns = relationship("users", cascade="all, delete")
