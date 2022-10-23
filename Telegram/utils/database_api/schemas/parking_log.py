from sqlalchemy import BigInteger, Column, ForeignKey, TIMESTAMP, String, sql

from utils.database_api.database_gino import TimeDatabaseModel


class ParkingLog(TimeDatabaseModel):
    __tablename__ = 'parking_logs'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    time_from_user = Column(TIMESTAMP)
    initials = Column(String, ForeignKey('users.id'))

    query: sql.insert
