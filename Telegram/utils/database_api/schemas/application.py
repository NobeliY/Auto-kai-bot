from sqlalchemy import BigInteger, Column, String, select

from utils.database_api.database_gino import TimeDatabaseModel


class Application(TimeDatabaseModel):
    __tablename__ = 'applications'
    id = Column(BigInteger, primary_key=True, unique=True)
    initials = Column(String, primary_key=True)
    email = Column(String, primary_key=True)
    phoneNumber = Column(String, primary_key=True)
    group = Column(String, primary_key=True)
    stateNumber = Column(String, primary_key=True)

    query: select
