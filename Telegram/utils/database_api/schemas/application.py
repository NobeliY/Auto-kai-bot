from sqlalchemy import BigInteger, Column, String, sql

from utils.database_api.database_gino import TimeDatabaseModel


class Application(TimeDatabaseModel):
    __tablename__ = 'applications'
    id = Column(BigInteger, primary_key=True, unique=True)
    fully_name = Column(String, primary_key=True)
    email = Column(String, primary_key=True)
    group = Column(String, primary_key=True)
    state_number = Column(String, primary_key=True)

    query: sql.insert
