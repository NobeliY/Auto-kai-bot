import logging as logger

from app import bot
from aiogram import types, Dispatcher
import aiogram.utils.exceptions as exceptions
from colorama import Fore

from Data import admins
from Handler.handler import register_handlers
from utils.database_api.database_gino import on_startup, on_close
from utils.database_api.quick_commands import get_users_info
from utils.shared_methods.default import set_on_startup_users


async def get_default_commands(dp: Dispatcher) -> None:
    logger.warning(f"Default commands: {dp}")
    try:
        on_close()
    except Exception as _ex:
        logger.info(f"{Fore.LIGHTRED_EX}{_ex} | On Close Exception {Fore.RESET}")
    await on_startup()
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Начало Работы / Обновить бота."),
            types.BotCommand("application", "Заявление."),
            types.BotCommand("help", "Инструкция по эксплуатации. 🧐")
        ]
    )
    set_on_startup_users([
        user.id for user in await get_users_info()
    ])
    logger.info(f"{Fore.GREEN}Бот запущен{Fore.RESET}!")

    for admin_id in admins:
        try:
            await bot.send_message(chat_id=admin_id, text=" Бот возобновил работу.")
        except exceptions.ChatNotFound:
            logger.error(f"{Fore.RED}Нет чата с {admin_id}{Fore.RESET}!")
    register_handlers(dp=dp)
    logger.info(f"{Fore.LIGHTGREEN_EX}Register handlers job done{Fore.RESET}!")
