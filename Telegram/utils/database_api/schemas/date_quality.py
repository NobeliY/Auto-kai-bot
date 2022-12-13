from sqlalchemy import Column, BigInteger, ForeignKey, Integer, sql, String
from utils.database_api.database_gino import BaseModel


class DateQuality(BaseModel):
    __tablename__ = 'date_quality'
    id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    times = Column(String, primary_key=True)
    count = Column(Integer, primary_key=True)

    query: sql.select
