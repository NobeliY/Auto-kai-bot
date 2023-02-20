from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from utils.database_api.database_sqlalchemy import Base


class DateQuality(Base):
    __tablename__ = "date_quality"
    id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    times: Mapped[str]
    count: Mapped[int]
    def __repr_(self) -> str:
        return f"id={self.id}, times={self.times}, count={self.count}."

