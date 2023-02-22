from datetime import timezone, timedelta, datetime
import logging as logger
import re
from typing import List

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from colorama import Fore
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from utils.database_api.schemas.application import Application
from utils.database_api.database_sqlalchemy import database
from utils.database_api.schemas.date_quality import DateQuality
from utils.database_api.schemas.user import User

_offset = timezone(timedelta(hours=3))


async def add_application(user_id: int, initials: str, email: str,
                          phone_number: str, group: str, state_number: str):
    try:
        application = Application(id=user_id, initials=initials, email=email,
                                  phoneNumber=phone_number, group=group, stateNumber=state_number)
        database.add(application)
        await database.commit()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} Application not created{Fore.RESET}!")


async def add_ready_application(application: Application):
    try:
        database.add(application)
        await database.commit()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} Application not created{Fore.RESET}!")


async def get_count_of_applications() -> int | None:
    applications_count = select(Application).count()
    return applications_count


async def get_application() -> Application | None:
    try:
        application = await database.select(Application).one()
        return application
    except MultipleResultsFound as multipleResultsFoundException:
        logger.error(f"{Fore.RED} Caught {multipleResultsFoundException} {Fore.RESET}")
    except NoResultFound as noResultFound:
        return None

async def get_all_applications() -> List[Application] | None:
    return await database.query(Application).all()


async def drop_application(application: Application) -> bool:
    return  database.query(application).delete()


async def get_users_info() -> List[User] | None:
    return database.query(User).all()


async def get_users_shortly_info() -> str | None:
    filtered_users = await filter_users_shortly_info(await get_users_info())
    return f"Всего в БД: <b>{database.query(User).count()}</b>\n" \
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


async def get_users_by_initials(initials):
    return database.query(User).where(User.initials.like(f"%{initials}%")).all()


async def delete_user_by_initials_command(user: User):
    database.query(user).delete()
    # await user.delete()


async def get_users_by_group(group: str) -> List[User] | None:
    return database.query(User).where(User.group == group).all()


async def delete_users_by_group(users: List[User]):

    for user in users:
        try:
            database.query(user).delete()
            # await user.delete()
        except ForeignKeyViolationError as foreignKeyViolationEr:
            logger.warning(f"{Fore.LIGHTYELLOW_EX}{user.initials} {Fore.LIGHTGREEN_EX} :"
                           f"try to delete: {Fore.YELLOW}{foreignKeyViolationEr}")
            await user.foreigns.delete()


async def add_user(user_id: int, initials: str, email: str,
                   phone_number: str, group: str, state_number: str, access: str):
    try:
        user = User(id=user_id, initials=initials, email=email, phoneNumber=phone_number, group=group,
                    stateNumber=state_number, access=access)
        database.add(user).commit()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} User not created{Fore.RESET}!")


async def get_user(user_id: int) -> User | None:
    user = database.query(User).where(User.id == user_id).first()
    return user if user is not None else None


async def get_date_quality_from_user(user_id: int):
    return database.query(DateQuality).where(DateQuality.id == user_id).first()


async def rebase_date_quality_from_user(user_id: int):
    date_quality = await get_date_quality_from_user(user_id=user_id)
    await date_quality.delete()
    return True


async def set_date_quality_from_user(user_id: int, count: int = 1) -> bool:
    try:
        time_now = datetime.now(tz=_offset).strftime("%d %m %Y %H %M")
        date_quality = DateQuality(id=user_id, times=time_now, count=count)
        database.add(date_quality).commit()
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
    database.query(preview_date_quality).update(count=preview_date_quality.count + 1)
    return True


async def check_admin(admin_id: int) -> bool:
    user = database.query(User).where(User.id == admin_id).first()
    try:
        return True if user.access == 'A' else False
    except AttributeError:
        return False
