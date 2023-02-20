from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, Relationship

from utils.database_api.database_sqlalchemy import TimeDatabaseModel


class User(TimeDatabaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    initials: Mapped[Optional[str]]
    email: Mapped[str]
    phoneNumber: Mapped[str]
    group: Mapped[str]
    stateNumber: Mapped[str]
    access: Mapped[str]

    foreigns: Mapped[Relationship] = relationship("users", cascade="all, delete")

    def __repr_(self) -> str:
        return f"id={self.id}, initials={self.initials}, email={self.email}," \
               f"phoneNumber={self.phoneNumber}, group={self.group}," \
               f"stateNumber={self.stateNumber}, access={self.access}."

