from datetime import datetime

from colorama import Fore

from Data import admins
from Handler.handler import register_handlers
from app import bot
from aiogram import types, Dispatcher
import aiogram.utils.exceptions as exceptions

from utils.database_api.database_gino import on_startup, on_close


async def get_default_commands(dp: Dispatcher):
    try:
        await on_close(dp)
    except Exception as _ex:
        print(Fore.LIGHTRED_EX + f"{_ex} | On Close Exception" + Fore.RESET)
    await on_startup(dp)
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Начало Работы / Обновить бота."),
            types.BotCommand("application", "Заявление."),
            types.BotCommand("help", "Инструкция по эксплуатации. 🧐")
        ]
    )
    print(Fore.GREEN + f"{datetime.now()}: Бот запущен" + Fore.RESET)

    for admin_id in admins:
        try:
            await bot.send_message(chat_id=admin_id, text=" Бот запущен.")
        except exceptions.ChatNotFound:
            print(Fore.RED + f"{datetime.now()}: Нет чата с {admin_id}" + Fore.RESET)
    register_handlers(dp=dp)

