from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ParseMode, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound

from Handler.default import get_access_level, soon_info
from Keyboard.Inline import change_info_menu
from app import dp
from states import UserState, Admins
from utils.database_api.quick_commands import get_user
from Data import __all_states__


@dp.message_handler(Text(equals="Информация о себе", ignore_case=True),
                    state=UserState.all_states)
@dp.message_handler(Text(equals="Информация о себе", ignore_case=True),
                    state=Admins.all_states)
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
        parse_mode=ParseMode.HTML,
        reply_markup=change_info_menu
    )
    await message.delete()


@dp.callback_query_handler(Text(equals="change_info_menu"),
                           state=__all_states__)
async def change_user_info(query: CallbackQuery, state: FSMContext):
    try:
        await query.message.delete()
        await query.message.answer(await soon_info())
    except MessageToDeleteNotFound:
        print("| Try delete Message")


@dp.message_handler(Text(equals="свободные места", ignore_case=True),
                    state=__all_states__)
async def get_free_positions(message: Message):
    await message.answer(await soon_info())
    await message.delete()
