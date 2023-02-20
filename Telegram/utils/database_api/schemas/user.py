from typing import Optional

from sqlalchemy import BigInteger, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, Relationship

from utils.database_api.schemas.database_sqlalchemy import TimeDatabaseModel


class User(TimeDatabaseModel):
    __tablename__ = "users"
    id: Mapped[BigInteger] = mapped_column(primary_key=True)
    initials: Mapped[Optional[str]]
    email: Mapped[str]
    phoneNumber: Mapped[str]
    group: Mapped[str]
    stateNumber: Mapped[str]
    access: Mapped[str]
    # = mapped_column(primary_key=True)

    query: select
    foreigns: Relationship = relationship("users", cascade="all, delete")

    def __repr_(self) -> str:
        return f"id={self.id}, initials={self.initials}, email={self.email}," \
               f"phoneNumber={self.phoneNumber}, group={self.group}," \
               f"stateNumber={self.stateNumber}, access={self.access}."

