import datetime

from Data.config import TIME_RANGE
from utils.database_api.database_gino import database
from utils.database_api.quick_commands import get_user
from utils.database_api.schemas.user import User


class RequestController:

    def __init__(self, user_id: int, attempts: int = 0):
        self.attempts = attempts
        self.user_id = user_id

    async def check_user_on_database(self) -> str | None:
        user = await get_user(user_id=self.user_id)
        return user.access if user is not None else None

    @staticmethod
    async def check_time(access_level: str) -> bool:
        activate_on_level = ['S', 'I']
        if access_level not in activate_on_level:
            return True
        offset = datetime.timezone(datetime.timedelta(hours=3))
        time_now = datetime.datetime.now(tz=offset).time()
        if TIME_RANGE[0] > time_now or time_now > TIME_RANGE[1]:
            return False
        return True
