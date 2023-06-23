import logging
import re
from enum import Enum
# from typing import List, Dict

from aiogram import types

import pandas as pd
from aiogram.utils.exceptions import ChatNotFound
from beartype import beartype
from beartype.typing import Dict, List

from Data.config import USER_XLSX_PATH
from Keyboard.Inline.user_keyboard import close_inline_keyboard
from Keyboard.Reply import student_menu, teacher_menu, employee_menu, admin_menu
from app import bot
from utils.database_api.quick_commands import get_users_info
from utils.database_api.schemas import User
from utils.request_api.Request_controller import RequestController


@beartype
async def soon_info() -> str:
    return "Эта функция скоро появится."


@beartype
def return_user_checked(user_registered: bool = True) -> str:
    return f"Открыл!" if user_registered else f"Добро пожаловать! \n" \
                                              f"Вы <b>не зарегистрированы</b>." \
                                              f"Пожалуйста, отправьте заявку: <b>/application</b>."


@beartype
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


@beartype
def get_access_level(access: str) -> str:
    dict_user_access_level = {
        'S': 'Студент',
        'I': 'Студент',
        'T': 'Преподаватель',
        'E': 'Сотрудник',
        'A': 'Администратор'
    }
    return dict_user_access_level[access]


@beartype
class Level(Enum):
    S = 'student'
    I = 'student_plus'
    T = 'teacher'
    E = 'employee'
    A = 'administrator'


@beartype
async def get_admin_level(request_controller: RequestController) -> bool:
    return await request_controller.check_user_on_database() == 'A'


_on_startup_users_id_list_: List[int] | None = None


@beartype
def on_startup_users() -> List[int]:
    return _on_startup_users_id_list_


@beartype
def set_on_startup_users(users_id: List[int]) -> None:
    global _on_startup_users_id_list_
    _on_startup_users_id_list_ = users_id


@beartype
def check_initials(initials: str) -> bool:
    return bool(re.fullmatch(r"^[А-Яа-яA-Za-z ]+", initials))


@beartype
def check_email(email: str) -> bool:
    """
    search by regex email ?
    """
    return bool(re.search(r"[^@]+@[^@]+\.[^@]+", email))


@beartype
def check_phone(phone: str) -> bool:
    """
    full match by regex phone ?
    """
    return bool(re.fullmatch(r"\d{11}", phone))


@beartype
def check_state_number(state_number: str) -> bool:
    """
    search state number by regex ?
    """
    return bool(re.search(r"\w\d{3}\w{2}\|\d", state_number))


@beartype
async def get_fully_info() -> None:
    users: List[User] = await get_users_info()
    data_dict: Dict[str, List] = {
        "Telegram ID": [],
        "ФИО": [],
        "Почта": [],
        "Группа": [],
        "Номер телефона": [],
        "Гос. номер используемого транспорта": [],
        "Уровень": []
    }
    for user in users:
        data_dict["Telegram ID"].append(user.id)
        data_dict["ФИО"].append(user.initials)
        data_dict["Почта"].append(user.email)
        data_dict["Группа"].append(user.group)
        data_dict["Номер телефона"].append(user.phoneNumber)
        data_dict["Гос. номер используемого транспорта"].append(user.stateNumber)
        data_dict["Уровень"].append(get_access_level(user.access))

    df: pd.DataFrame = pd.DataFrame(data=data_dict)
    df.to_excel(USER_XLSX_PATH, sheet_name='Users', index=False)


@beartype
async def user_to_str(user: User) -> str:
    return f"Telegram ID: <b>{user.id}</b>\n" \
           f"ФИО: <b>{user.initials}</b>\n" \
           f"Почта: <b>{user.email}</b>\n" \
           f"Группа: <b>{user.group}</b>\n" \
           f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n" \
           f"Уровень: <b>{get_access_level(user.access)}</b>"


@beartype
async def send_user_application_info(telegram_id: int, message: str) -> None:
    try:
        await bot.send_message(chat_id=telegram_id, text=message, reply_markup=close_inline_keyboard)
    except ChatNotFound:
        logging.error(f"Chat not found: {telegram_id} | Message: {message}")
