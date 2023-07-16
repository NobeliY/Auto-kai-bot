import datetime
import logging as logger
from typing import List
from colorama import Fore
import sqlalchemy as sa
from gino import Gino
from Data import POSTGRES_URL
from utils.database_api.quick_commands import get_admins_id

database: Gino = Gino()


class BaseModel(database.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimeDatabaseModel(BaseModel):
    __abstract__ = True

    created_at = database.Column(database.DateTime(True), server_default=database.func.now())
    updated_at = database.Column(
        database.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=database.func.now(),
    )


async def on_startup():
    logger.info(f"{Fore.GREEN}Подключение к БД PostgreSQL Server{Fore.RESET}")
    await database.set_bind(POSTGRES_URL)
    return await get_admins_id()


def on_close():
    database.pop_bind()
