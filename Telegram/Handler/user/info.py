import logging as logger

from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound
from colorama import Fore

from Keyboard.Inline import change_info_menu

from utils.database_api.quick_commands import get_user
from utils.shared_methods.default import soon_info, get_access_level


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
        reply_markup=change_info_menu
    )
    await message.delete()


async def close_user_info(query: CallbackQuery):
    try:
        await query.message.delete()
    except MessageToDeleteNotFound:
        logger.error(f"{Fore.LIGHTRED_EX}{query.message.from_id} | Try delete message with close info.")


async def change_user_info(query: CallbackQuery):
    try:
        await query.message.delete()
        await query.message.answer(await soon_info())
    except MessageToDeleteNotFound:
        pass


async def get_free_positions(message: Message):
    await message.answer(await soon_info())
    await message.delete()
