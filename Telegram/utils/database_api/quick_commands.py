import logging
from datetime import timezone, timedelta, datetime
import logging as logger
import re
from typing import List, Union, Dict

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from colorama import Fore
from sqlalchemy import TIMESTAMP, and_

from utils.database_api.database_gino import database
from utils.database_api.schemas import ApplicationChange, Application, DateQuality, User, ParkingLog, AiogramState, \
    AiogramData, AiogramBucket

_offset = timezone(timedelta(hours=3))


async def add_application(user_id: int, initials: str, email: str,
                          phone_number: str, group: str, car_mark: str, state_number: str,
                          change_ap: bool = False) -> None:
    application: Union[Application, ApplicationChange, None] = None
    try:
        application = Application(
            id=user_id,
            initials=initials,
            email=email,
            phoneNumber=phone_number,
            group=group,
            car_mark=car_mark,
            stateNumber=state_number
        ) if not change_ap else \
            ApplicationChange(
                id=user_id,
                initials=initials,
                email=email,
                phoneNumber=phone_number,
                group=group,
                car_mark=car_mark,
                stateNumber=state_number
            )
        await application.create()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} {type(application)} not created{Fore.RESET}!")


async def get_serialized_application(application_dict: Dict, change_ap: bool = False) -> Union[
    Application, ApplicationChange
]:
    return Application(
        id=application_dict["id"],
        initials=application_dict["initials"],
        email=application_dict["email"],
        phoneNumber=application_dict["phoneNumber"],
        group=application_dict["group"],
        car_mark=application_dict["car_mark"],
        stateNumber=application_dict["stateNumber"]
    ) if not change_ap else \
        ApplicationChange(
            id=application_dict["id"],
            initials=application_dict["initials"],
            email=application_dict["email"],
            phoneNumber=application_dict["phoneNumber"],
            group=application_dict["group"],
            car_mark=application_dict["car_mark"],
            stateNumber=application_dict["stateNumber"]
        )


async def add_ready_application(application: Union[Application, ApplicationChange]) -> None:
    try:
        await application.create()
    except UniqueViolationError:
        logger.warning(f"{Fore.LIGHTGREEN_EX} {type(application)} not created{Fore.RESET}!")


async def get_count_of_applications(change_ap: bool = False) -> int | None:
    return await database.func.count(Application.id).gino.scalar() if not change_ap else \
        await database.func.count(ApplicationChange.id).gino.scalar()


async def get_application(change_ap: bool = False) -> Union[Application, ApplicationChange, None]:
    return await Application.query.gino.first() if not change_ap else \
        await ApplicationChange.query.gino.first()


async def get_all_applications(change_ap: bool = False) -> Union[List[Application], List[ApplicationChange], None]:
    return await Application.query.gino.all() if not change_ap else \
        await ApplicationChange.query.gino.all()


async def get_required_application(tg_id: int, change_app: bool = False) -> Union[
    Application, ApplicationChange, None]:
    return await ApplicationChange.query.where(ApplicationChange.id == tg_id).gino.first() if change_app else await \
        Application.query.where(ApplicationChange.id == tg_id).gino.first()


async def drop_application(application: Union[Application, ApplicationChange]) -> bool:
    if application is None:
        return False
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
            [0 if re.findall(r"\d-\d", user.group) or re.findall(r"Преподаватель", user.group) else 1 for user in
             users]
        )
    }


async def get_users_by_initials(initials) -> List[User] | None:
    return await User.query.where(User.initials.like(f"%{initials}%")).gino.all()


async def get_serialized_user(user_dict: Dict) -> User:
    return User(id=user_dict["id"], initials=user_dict["initials"], email=user_dict["email"],
                phoneNumber=user_dict["phoneNumber"], group=user_dict["group"],
                stateNumber=user_dict["stateNumber"], access=user_dict["access"])


async def delete_user_by_initials_command(user: Union[User, Dict]) -> None:
    if user is dict:
        user = User(
            id=user["id"],
            initials=user["initials"],
            email=user["email"],
            phoneNumber=user["phoneNumber"],
            group=user["group"],
            car_mark=user["car_mark"],
            stateNumber=user["stateNumber"],
            access=user["access"]
        )
    try:
        await user.delete()
    except ForeignKeyViolationError as foreignKeyViolationEr:
        logger.warning(f"{Fore.LIGHTYELLOW_EX}{user.initials} {Fore.LIGHTGREEN_EX}: "
                       f"try to delete: {Fore.YELLOW}{foreignKeyViolationEr}")
        await delete_user(user=user)


async def get_users_by_group(group: str) -> Union[List[User], None]:
    return await User.query.where(User.group == group).gino.all()


async def get_users_by_car_mark(car_mark: str) -> Union[List[User], None]:
    return await User.query.where(User.car_mark == car_mark).gino.all()


async def get_user_by_state_number(state_number: str) -> Union[List[User], None]:
    return await User.query.where(User.stateNumber == state_number).gino.first()


async def get_user_by_id(user_id: int) -> Union[User, None]:
    return await User.query.where(User.id == user_id).gino.first()


async def get_users_by_phone_number(phone_number: str) -> Union[List[User], None]:
    return await User.query.where(User.phoneNumber == phone_number).gino.all()


async def get_all_users() -> Union[List[User], None]:
    return await User.query.gino.all()


async def get_users_by_access(access: str) -> Union[List[User], None]:
    return await User.query.where(User.access == access).gino.all()


async def delete_user(user: User) -> None:
    if user is None:
        return
    await drop_application(await get_required_application(user.id, change_app=True))
    await rebase_date_quality_from_user(user.id)
    await delete_parking_log(user_id=user.id)
    await user.delete()


async def delete_users_by_group(users: List[User]) -> None:
    for user in users:
        try:
            await user.delete()
        except ForeignKeyViolationError as foreignKeyViolationEr:
            logger.warning(f"{Fore.LIGHTYELLOW_EX}{user.initials} {Fore.LIGHTGREEN_EX} :"
                           f"try to delete: {Fore.YELLOW}{foreignKeyViolationEr}")
            await delete_user(user=user)


async def add_user(user_id: int, initials: str, email: str,
                   phone_number: str, group: str,
                   car_mark: str, state_number: str, access: str) -> None:
    try:
        user = User(id=user_id, initials=initials, email=email, phoneNumber=phone_number, group=group,
                    car_mark=car_mark, stateNumber=state_number, access=access)
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
    if date_quality is None:
        return False
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


async def add_parking_log(user_id: int, initials: str) -> None:
    try:
        time_now = datetime.now(tz=_offset).strftime("%d %m %Y %H %M")
        parking_log = ParkingLog(
            user_id=user_id,
            initials=initials,
            time_from_user=time_now
        )
        await parking_log.create()
    except UniqueViolationError:
        pass


async def get_parking_log(user_id: int) -> List[ParkingLog] | None:
    return await ParkingLog.query.where(ParkingLog.id == user_id).gino.all()


async def delete_parking_log(user_id: int) -> None:
    parking_logs = await get_parking_log(user_id=user_id)
    if parking_logs is None:
        return
    for parking_log in parking_logs:
        await parking_log.delete()


async def check_admin(admin_id: int) -> bool:
    user = await User.query.where(User.id == admin_id).gino.first()
    try:
        return True if user.access == 'A' else False
    except AttributeError:
        return False


async def get_admins_id() -> List[int]:
    admins = await User.query.where(User.access == 'A').gino.all()
    return [
        admin.id for admin in admins
    ]


""" Aiogram save FSM states """


async def add_aiogram_state(user: int, chat: int, state: str) -> None:
    aiogram_state = AiogramState(
        user=user,
        chat=chat,
        state=state
    )
    await aiogram_state.create()


async def get_aiogram_state(user: int, chat: int) -> Union[AiogramState, None]:
    return await AiogramState.query.where(and_(AiogramState.user == user, AiogramState.chat == chat)).gino.first()


async def delete_aiogram_state(user: int, chat: int) -> None:
    aiogram_state = await get_aiogram_state(user=user, chat=chat)
    if not aiogram_state:
        return
    await aiogram_state.delete()


async def get_all_aiogram_states() -> List[AiogramState]:
    return await AiogramState.query.gino.all()


async def delete_all_aiogram_states() -> None:
    aiogram_states: Union[List[AiogramState], None] = await get_all_aiogram_states()
    if not aiogram_states:
        return
    for aiogram_state in aiogram_states:
        await aiogram_state.delete()


async def add_aiogram_data(user: int, chat: int, data: dict) -> None:
    aiogram_data = AiogramData(
        user=user,
        chat=chat,
        data=data
    )
    await aiogram_data.create()


async def get_aiogram_data(user: int, chat: int) -> Union[AiogramData, None]:
    return await AiogramData.query.where(and_(AiogramData.user == user, AiogramData.chat == chat)).gino.first()


async def delete_aiogram_data(user: int, chat: int) -> None:
    aiogram_data = await get_aiogram_data(user=user, chat=chat)
    if not aiogram_data:
        return
    await aiogram_data.delete()


async def get_all_aiogram_datas() -> List[AiogramData]:
    return await AiogramData.query.gino.all()


async def delete_all_aiogram_datas() -> None:
    aiogram_datas: Union[List[AiogramData], None] = await get_all_aiogram_datas()
    if not aiogram_datas:
        return
    for aiogram_data in aiogram_datas:
        await aiogram_data.delete()


async def add_aiogram_bucket(user: int, chat: int, bucket: dict) -> None:
    aiogram_bucket = AiogramBucket(
        user=user,
        chat=chat,
        bucket=bucket
    )
    await aiogram_bucket.create()


async def get_aiogram_bucket(user: int, chat: int) -> Union[AiogramBucket, None]:
    return await AiogramBucket.query.where(
        and_(AiogramBucket.user == user, AiogramBucket.chat == chat)).gino.first()


async def delete_aiogram_bucket(user: int, chat: int) -> None:
    aiogram_bucket = await get_aiogram_bucket(user=user, chat=chat)
    await aiogram_bucket.delete()


async def get_all_aiogram_buckets() -> List[AiogramBucket]:
    return await AiogramBucket.query.gino.all()


async def delete_all_aiogram_buckets() -> None:
    aiogram_buckets: Union[List[AiogramBucket], None] = await get_all_aiogram_buckets()
    if not aiogram_buckets:
        return
    for aiogram_bucket in aiogram_buckets:
        await aiogram_bucket.delete()


async def drop_aiogram_save_data_tables(full: bool) -> None:
    await delete_all_aiogram_states()
    if full:
        await delete_all_aiogram_datas()
        await delete_all_aiogram_buckets()
