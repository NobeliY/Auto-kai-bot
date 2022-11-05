from datetime import datetime

from colorama import Fore

from Data import admins
from Keyboard import student_menu, teacher_menu, employee_menu, admin_menu
from app import bot, dp
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
            types.BotCommand("help", "Инструкция по эксплуатации.")
        ]
    )
    print(Fore.GREEN + f"{datetime.now()}: Бот запущен" + Fore.RESET)

    for admin_id in admins:
        try:
            await bot.send_message(chat_id=admin_id, text=" Бот запущен.")
        except exceptions.ChatNotFound:
            print(Fore.RED + f"{datetime.now()}: Нет чата с {admin_id}" + Fore.RESET)


def get_access_level(access: str) -> str:
    dict_user_access_level = {
        'S': 'Студент',
        'I': 'Студент',
        'T': 'Преподаватель',
        'E': 'Сотрудник',
        'A': 'Администратор'
    }
    return dict_user_access_level[access]


def get_reply_keyboard(access: str) -> types.ReplyKeyboardMarkup:
    match access:
        case 'S':
            return student_menu
        case 'I':
            return student_menu
        case 'T':
            return teacher_menu
        case 'E':
            return employee_menu
        case 'A':
            return admin_menu


def return_user_checked(user_registered: bool) -> str:
    return f"Открыл!" if user_registered else f"Добро пожаловать! \n" \
                                              f"Вы <b>не зарегистрированы</b>." \
                                              f"Пожалуйста, отправьте заявку: <b>/application</b>."


async def soon_info() -> str:
    return "Эта функция скоро появится."
