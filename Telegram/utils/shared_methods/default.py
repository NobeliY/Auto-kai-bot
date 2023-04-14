import re
from enum import Enum
from typing import List

from aiogram import types
from Keyboard.Reply import student_menu, teacher_menu, employee_menu, admin_menu
from utils.request_api.Request_controller import RequestController


async def soon_info() -> str:
    return "Эта функция скоро появится."


def return_user_checked(user_registered: bool = True) -> str:
    return f"Открыл!" if user_registered else f"Добро пожаловать! \n" \
                                              f"Вы <b>не зарегистрированы</b>." \
                                              f"Пожалуйста, отправьте заявку: <b>/application</b>."


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


def get_access_level(access: str) -> str:
    dict_user_access_level = {
        'S': 'Студент',
        'I': 'Студент',
        'T': 'Преподаватель',
        'E': 'Сотрудник',
        'A': 'Администратор'
    }
    return dict_user_access_level[access]


class Level(Enum):
    S = 'student'
    I = 'student_plus'
    T = 'teacher'
    E = 'employee'
    A = 'administrator'


async def get_admin_level(request_controller: RequestController) -> bool:
    return await request_controller.check_user_on_database() == 'A'


_on_startup_users_id_list_: List[int] | None = None


def on_startup_users() -> List[int]:
    return _on_startup_users_id_list_


def set_on_startup_users(users_id: List[int]) -> None:
    global _on_startup_users_id_list_
    _on_startup_users_id_list_ = users_id


def check_initials(initials: str) -> bool:
    return bool(re.fullmatch(r"^[А-Яа-я ]+", initials))


def check_email(email: str) -> bool:
    """
    search by regex email ?
    """
    return bool(re.search(r"[^@]+@[^@]+\.[^@]+", email))


def check_phone(phone: str) -> bool:
    """
    full match by regex phone ?
    """
    return bool(re.fullmatch(r"\d{11}", phone))


def check_state_number(state_number: str) -> bool:
    """
    search state number by regex ?
    """
    return bool(re.search(r"\w\d{3}\w{2}\|\d", state_number))
