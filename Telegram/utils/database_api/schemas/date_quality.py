from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP, Integer, sql

from utils.database_api.database_gino import TimeDatabaseModel


class DateQuality(TimeDatabaseModel):
    __tablename__ = 'date_quality'
    id = Column(BigInteger, ForeignKey('users.id'))
    times = Column(TIMESTAMP)
    count = Column(Integer)

    query: sql.select
