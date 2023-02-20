from sqlalchemy import select, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from utils.database_api.database_sqlalchemy import TimeDatabaseModel


class Application(TimeDatabaseModel):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    initials: Mapped[str]
    email: Mapped[str]
    phoneNumber: Mapped[str]
    group: Mapped[str]
    stateNumber: Mapped[str]

    def __repr_(self) -> str:
        return f"id={self.id}, initials={self.initials}, email={self.email}," \
               f"phoneNumber={self.phoneNumber}, group={self.group}," \
               f"stateNumber={self.stateNumber}."
