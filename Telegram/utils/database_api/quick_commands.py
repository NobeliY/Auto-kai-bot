from datetime import timezone, timedelta, datetime

from asyncpg import UniqueViolationError

from utils.database_api.database_gino import database
from utils.database_api.schemas.application import Application
from utils.database_api.schemas.date_quality import DateQuality
from utils.database_api.schemas.user import User


# TODO -------------- Application
async def add_application(user_id: int, initials: str, email: str,
                          phone_number: str, group: str, state_number: str):
    try:
        application = Application(id=user_id, initials=initials, email=email,
                                  phoneNumber=phone_number, group=group, stateNumber=state_number)
        await application.create()
    except UniqueViolationError:
        print("Application not created!")


async def get_count_of_applications(admin_id: int) -> int | None:
    if await check_admin(admin_id=admin_id):
        applications_count = await database.func.count(Application.id).gino.scalar()
        return applications_count
    return None


# TODO -------------- User
async def get_users_info(admin_id: int) -> User | None:
    if await check_admin(admin_id=admin_id):
        return await User.query.gino.all()
    return None


async def add_user(user_id: int, initials: str, email: str,
                   phone_number: str, group: str, state_number: str, access: str):
    try:
        user = User(id=user_id, initials=initials, email=email, phoneNumber=phone_number, group=group,
                    stateNumber=state_number, access=access)
        await user.create()
    except UniqueViolationError:
        print("User not created! ")


async def get_user(user_id: int) -> User | None:
    user = await User.query.where(User.id == user_id).gino.first()
    return user if user is not None else None


# TODO -------------- Date Quality
offset = timezone(timedelta(hours=3))


async def get_date_quality_from_user(user_id: int):
    return await DateQuality.query.where(DateQuality.id == user_id).gino.first()


async def rebase_date_quality_from_user(user_id: int):
    date_quality = await get_date_quality_from_user(user_id=user_id)
    await date_quality.delete()
    return True


async def set_date_quality_from_user(user_id: int, count: int = 1) -> bool:
    try:
        time_now = datetime.now(tz=offset).strftime("%d %m %Y %H %M")
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
