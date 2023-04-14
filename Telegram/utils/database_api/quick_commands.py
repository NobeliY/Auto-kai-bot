from datetime import timezone, timedelta, datetime
import logging as logger
import re
from typing import List, Union

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from colorama import Fore

from utils.database_api.database_gino import database
from utils.database_api.schemas import ApplicationChange
from utils.database_api.schemas.application import Application
from utils.database_api.schemas.date_quality import DateQuality
from utils.database_api.schemas.user import User

_offset = timezone(timedelta(hours=3))


async def add_application(user_id: int, initials: str, email: str,
                          phone_number: str, group: str, state_number: str) -> None:
    try:
        application = Application(id=user_id, initials=initials, email=email,
                                  phoneNumber=phone_number, group=group, stateNumber=state_number)
        await application.create()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} Application not created{Fore.RESET}!")


async def add_change_application(user_id: int, initials: str, email: str,
                                 phone_number: str, group: str, state_number: str) -> None:
    try:
        change_application: ApplicationChange = ApplicationChange(
            id=user_id,
            initials=initials,
            email=email,
            phoneNumber=phone_number,
            group=group,
            stateNumber=state_number
        )
        await change_application.create()
    except UniqueViolationError:
        logger.warning(f"[{user_id}] -> {Fore.LIGHTGREEN_EX} Change Application not created{Fore.RESET}!")


async def add_ready_application(application: Application | ApplicationChange) -> None:
    try:
        await application.create()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} {type(application)} not created{Fore.RESET}!")


async def get_count_of_applications() -> int | None:
    applications_count = await database.func.count(Application.id).gino.scalar()
    return applications_count


async def get_count_of_change_application() -> int | None:
    return await database.func.count(ApplicationChange.id).gino.scalar()


async def get_application() -> Application | None:
    return await Application.query.gino.first()


async def get_all_applications() -> List[Application] | None:
    return await Application.query.gino.all()


async def get_all_change_applications() -> List[ApplicationChange] | None:
    return await ApplicationChange.query.gino.all()


async def get_required_application(tg_id: int, change_app: bool = False) -> Union[Application, ApplicationChange, None]:
    return await ApplicationChange.query.where(ApplicationChange.id == tg_id).gino.first() if change_app else await \
        Application.query.where(ApplicationChange.id == tg_id).gino.first()


async def drop_application(application: Application | ApplicationChange) -> bool:
    return await application.delete()


async def update_user(application: ApplicationChange) -> bool:
    _user = await get_user(application.id)
    update_data: dict = {key: value for key, value in application.__dict__['__values__'].items() if value}
    await User.update.values(update_data).where(User.id == _user.id).gino.status()
    return True


async def get_users_info() -> List[User] | None:
    return await User.query.gino.all()


async def get_users_shortly_info() -> str | None:
    filtered_users = await filter_users_shortly_info(await get_users_info())
    return f"Всего в БД: <b>{await database.func.count(User.id).gino.scalar()}</b>\n" \
           f"Из них: \n" \
           f"Студенты: <b>{filtered_users['Студенты']}</b>\n" \
           f"Преподаватели: <b>{filtered_users['Преподаватели']}</>\n" \
           f"Сотрудники: <b>{filtered_users['Сотрудники']}</b>"


async def filter_users_shortly_info(users: List[User]) -> dict:
    return {
        'Студенты': sum(
            [1 if re.findall(r"\d-\d", user.group) else 0 for user in users]
        ),
        'Преподаватели': sum(
            [1 if re.findall(r"Преподаватель", user.group) else 0 for user in users]
        ),
        'Сотрудники': sum(
            [0 if re.findall(r"\d-\d", user.group) or re.findall(r"Преподаватель", user.group) else 1 for user in users]
        )
    }


async def get_users_by_initials(initials) -> List[User] | None:
    return await User.query.where(User.initials.like(f"%{initials}%")).gino.all()


async def delete_user_by_initials_command(user: User) -> None:
    await user.delete()


async def get_users_by_group(group: str) -> List[User] | None:
    return await User.query.where(User.group == group).gino.all()


async def delete_users_by_group(users: List[User]) -> None:
    for user in users:
        try:
            await user.delete()
        except ForeignKeyViolationError as foreignKeyViolationEr:
            logger.warning(f"{Fore.LIGHTYELLOW_EX}{user.initials} {Fore.LIGHTGREEN_EX} :"
                           f"try to delete: {Fore.YELLOW}{foreignKeyViolationEr}")
            await user.foreigns.delete()


async def add_user(user_id: int, initials: str, email: str,
                   phone_number: str, group: str, state_number: str, access: str) -> None:
    try:
        user = User(id=user_id, initials=initials, email=email, phoneNumber=phone_number, group=group,
                    stateNumber=state_number, access=access)
        await user.create()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} User not created{Fore.RESET}!")


async def get_user(user_id: int) -> User | None:
    user = await User.query.where(User.id == user_id).gino.first()
    return user if user is not None else None


async def get_date_quality_from_user(user_id: int) -> DateQuality | None:
    return await DateQuality.query.where(DateQuality.id == user_id).gino.first()


async def rebase_date_quality_from_user(user_id: int) -> bool:
    date_quality = await get_date_quality_from_user(user_id=user_id)
    await date_quality.delete()
    return True


async def set_date_quality_from_user(user_id: int, count: int = 1) -> bool:
    try:
        time_now = datetime.now(tz=_offset).strftime("%d %m %Y %H %M")
        date_quality = DateQuality(id=user_id, times=time_now, count=count)
        await date_quality.create()
        return True
    except UniqueViolationError:
        return False


async def update_date_quality(user_id: int, reset: bool = False) -> bool:
    preview_date_quality = await get_date_quality_from_user(user_id=user_id)
    if preview_date_quality.count == 2 and not reset:
        return False
    if reset:
        await set_date_quality_from_user(user_id=user_id)
        return True
    await preview_date_quality.update(count=preview_date_quality.count + 1).apply()
    return True


async def check_admin(admin_id: int) -> bool:
    user = await User.query.where(User.id == admin_id).gino.first()
    try:
        return True if user.access == 'A' else False
    except AttributeError:
        return False
