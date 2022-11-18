from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ParseMode

from Handler.default import get_access_level, soon_info
from app import dp
from states import UserState, Admin
from utils.database_api.quick_commands import get_user


@dp.message_handler(Text(equals="Информация о себе", ignore_case=True),
                    state=UserState.all_states)
@dp.message_handler(Text(equals="Информация о себе", ignore_case=True),
                    state=Admin.all_states)
async def get_user_info(message: Message):
    user = await get_user(message.from_id)
    await message.answer(
        f"Информация о Вас! \n"
        f"Ваш Telegram ID: <b>{user.id}</b>\n"
        f"ФИО: <b>{user.initials}</b>\n"
        f"Почта: <b>{user.email}</b>\n"
        f"Номер телефона: <b>{user.phoneNumber}</b>\n"
        f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
        f"Уровень: <b>{get_access_level(user.access)}</b>\n",
        parse_mode=ParseMode.HTML
    )
    await message.delete()


@dp.message_handler(Text(equals="свободные места", ignore_case=True),
                    state=UserState.all_states)
@dp.message_handler(Text(equals="свободные места", ignore_case=True),
                    state=Admin.all_states)
async def get_free_positions(message: Message):
    await message.answer(await soon_info())
    await message.delete()
