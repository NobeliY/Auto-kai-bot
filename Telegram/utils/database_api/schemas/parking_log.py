from sqlalchemy import BigInteger, Column, TIMESTAMP, String, sql

from utils.database_api.database_gino import TimeDatabaseModel, database


class ParkingLog(TimeDatabaseModel):
    __tablename__ = 'parking_logs'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, database.ForeignKey('users.id'))
    time_from_user = Column(TIMESTAMP)
    initials = Column(String, database.ForeignKey('users.initials'))

    query: sql.insert

