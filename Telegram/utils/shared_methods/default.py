from enum import Enum

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


async def get_admin_level(request_controller: RequestController):
    return await request_controller.check_user_on_database() == 'A'
