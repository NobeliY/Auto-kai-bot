from sqlalchemy import BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from utils.database_api.database_sqlalchemy import TimeDatabaseModel


class ParkingLog(TimeDatabaseModel):
    __tablename__ = "parking_logs"
    id: Mapped[BigInteger] = mapped_column(primary_key=True)
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey("users.id"))
    time_from_user: Mapped[TIMESTAMP]
    initials: Mapped[str] = mapped_column(ForeignKey("users.initials"))

    def __repr__(self) -> str:
        return f"id={self.id}, user_id={self.user_id}," \
               f"time_from_user={self.time_from_user}," \
               f"initials={self.initials}."
