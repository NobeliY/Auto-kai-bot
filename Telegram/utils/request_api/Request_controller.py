from datetime import datetime, timedelta, timezone

from Data.config import TIME_RANGE
from utils.database_api.quick_commands import (
    get_user,
    get_date_quality_from_user,
    set_date_quality_from_user,
    update_date_quality,
    rebase_date_quality_from_user
)
from utils.request_api.SMTP_controller import SMTPController


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls)
        return cls._instances[cls]


class RequestController(Singleton):
    activate_on_level: list[str] = ['S', 'I']
    _offset = timezone(timedelta(hours=3))

    def __init__(self, user_id: int, attempts: int = 0):
        self.attempts = attempts
        self.user_id = user_id

    async def check_user_on_database(self) -> str | None:
        user = await get_user(user_id=self.user_id)
        return user.access if user is not None else None

    async def check_time(self, access_level: str) -> bool:
        if access_level not in self.activate_on_level:
            return True
        time_now = datetime.now(tz=self._offset).time()
        if TIME_RANGE[0] > time_now or time_now > TIME_RANGE[1]:
            return False
        return True

    async def check_date_quality(self) -> dict:
        preview_date_quality_from_user = await get_date_quality_from_user(self.user_id)
        if preview_date_quality_from_user is None:
            if await set_date_quality_from_user(user_id=self.user_id):
                return self.return_status_message("200-S")
            else:
                return self.return_status_message("500-C")

        time_now = datetime.now(tz=self._offset).strftime("%d %m %Y %H %M")
        time_now_split = self.rebase_time_list([
            int(datetime_item)
            for datetime_item in time_now.split(" ")
        ])
        preview_time = self.rebase_time_list(
            [int(datetime_item) for datetime_item in preview_date_quality_from_user.times.split(" ")])
        if preview_time["day"] != time_now_split["day"] \
                or preview_time["month"] != time_now_split["month"] \
                or preview_time["year"] != time_now_split["year"]:
            await update_date_quality(user_id=self.user_id, reset=True)
            return self.return_status_message("200-R")

        if time_now_split["minute"] > preview_time["minute"]:
            if time_now_split["minute"] - preview_time["minute"] > 3:
                await update_date_quality(user_id=self.user_id, reset=True)
                return self.return_status_message("200-U")
            if not await update_date_quality(user_id=self.user_id):
                """
                    Use SMTP to send e-mail.
                """
                user = await get_user(self.user_id)
                smtp = SMTPController(
                    fully_name=user.initials,
                    group=user.group,
                    date=f"{time_now_split['day']}.{time_now_split['month']}.{time_now_split['year']}",
                    first_time=f"{preview_time['hour']}:{preview_time['minute']}",
                    second_time=f"{time_now_split['hour']}:{time_now_split['minute']}",
                    phone=user.phoneNumber,
                    state_number=user.stateNumber,
                    email=user.email
                )
                smtp.build_message()
                smtp.send_message()

                await rebase_date_quality_from_user(user_id=self.user_id)
                return self.return_status_message("200-M")
        elif time_now_split["minute"] < preview_time["minute"]:
            if time_now_split["hour"] - preview_time["hour"] > 1:
                await update_date_quality(user_id=self.user_id, reset=True)
                return self.return_status_message("200-R")
            if 60 - preview_time["minute"] + time_now_split["minute"] > 3:
                await update_date_quality(user_id=self.user_id, reset=True)
                return self.return_status_message("200-R")
            await update_date_quality(user_id=self.user_id)
            return self.return_status_message("200-U")
        await update_date_quality(user_id=self.user_id)
        return self.return_status_message("200-S")

    @staticmethod
    def return_status_message(status_code: str) -> dict:
        status = status_code.split("-")
        match status[0]:
            case "200":
                match status[1].upper():
                    case "S":
                        return {
                            "status": 200,
                            "message": "Set up to Date Quality tables"
                        }
                    case "U":
                        return {
                            "status": 200,
                            "message": "Update to Date Quality tables"
                        }
                    case "R":
                        return {
                            "status": 200,
                            "message": "Re-create to Date Quality tables"
                        }
                    case "M":
                        return {
                            "status": 200,
                            "message": "Mail sent."
                        }
            case "400":
                pass
            case "500":
                match status[1].upper():
                    case "C":
                        return {
                            "status": 500,
                            "message": "Could not create a Date Quality"
                        }
                    case "M":
                        return {
                            "status": 504,
                            "message": "Mail error"
                        }

    @staticmethod
    def rebase_time_list(time_list: list) -> dict:
        return {
            "day": time_list[0],
            "month": time_list[1],
            "year": time_list[2],
            "hour": time_list[3],
            "minute": time_list[4]
        }
