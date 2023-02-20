import logging
import logging as logger

from colorama import Fore

from app import bot
from aiogram import types, Dispatcher
import aiogram.utils.exceptions as exceptions
from Data import admins
from Handler.handler import register_handlers

from utils.database_api.database_sqlalchemy import on_startup, on_close, create_async_database


async def get_default_commands(dp: Dispatcher):
    try:
        await on_close()
    except Exception as _ex:
        logger.info(f"{Fore.LIGHTRED_EX}{_ex} | On Close Exception {Fore.RESET}")
    logging.info(f"{Fore.GREEN}Подключение к БД. {Fore.RESET}")
    bot["session"] = await create_async_database()
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Начало Работы / Обновить бота."),
            types.BotCommand("application", "Заявление."),
            types.BotCommand("help", "Инструкция по эксплуатации. 🧐")
        ]
    )
    logger.info(f"{Fore.GREEN}Бот запущен{Fore.RESET}!")

    for admin_id in admins:
        try:
            await bot.send_message(chat_id=admin_id, text=" Бот возобновил работу.")
        except exceptions.ChatNotFound:
            logger.error(f"{Fore.RED}Нет чата с {admin_id}{Fore.RESET}!")
    register_handlers(dp=dp)
    logger.info(f"{Fore.LIGHTGREEN_EX}Register handlers job done{Fore.RESET}!")

