import asyncio
import datetime
import re
import threading
from threading import Thread
from time import sleep
from typing import Any

from Keyboard import student_menu, teacher_menu, employee_menu, admin_menu
# TODO: Import a Custom Modules
from app import bot, dp
from Data import admins
from states import ApplicationSubmission, UserState

# TODO: Import Aiogram
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import aiogram.utils.exceptions as exceptions

# TODO: Import and Init Colorama
from colorama import Fore

from utils.database_api.database_gino import on_startup, on_close
from utils.database_api.quick_commands import get_user
from utils.request_api.Request_controller import RequestController


def user_opened_task():
    sleep(20)


opened_loop = Thread(target=user_opened_task)


async def get_default_commands(dp: Dispatcher):
    try:
        await on_close(dp)
    except:
        print("On Close Exception")
    await on_startup(dp)
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Начало Работы / Обновить бота."),
            types.BotCommand("application", "Заявление."),
            types.BotCommand("help", "Инструкция по эксплуатации.")
        ]
    )
    print(Fore.GREEN + f"{datetime.datetime.now()}: Бот запущен")

    for admin_id in admins:
        try:
            await bot.send_message(chat_id=admin_id, text=" Бот запущен.")
        except exceptions.ChatNotFound:
            print(Fore.RED + F"{datetime.datetime.now()}: Нет чата с {admin_id}")


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


# TODO: Start
@dp.message_handler(Command("start"), state="*")
async def start(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await get_user(message.from_id)

    if user is None:
        await message.answer(return_user_checked(False), parse_mode=types.ParseMode.HTML,
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(f"Добро пожаловать! \n"
                             f"|{get_access_level(user.access)}| {user.initials}!\n"
                             f"Вызвана клавиатура с командами снизу!",
                             parse_mode=types.ParseMode.HTML, reply_markup=get_reply_keyboard(user.access))
        await UserState.in_active.set()
    # await state.finish()


# TODO: Reply Text
@dp.message_handler(state=UserState.in_active)
async def keyboard_on_registered_users(message: types.Message, state: FSMContext):
    activate_on_level = ['E', 'A']
    request_controller = RequestController(message.from_id)
    global opened_loop
    match message.text:
        case "Выйти":
            await state.finish()
        case "Открыть":
            if opened_loop.is_alive():
                await message.answer(F"Уже открыт")
            else:
                access = await request_controller.check_user_on_database()
                if access is not None:
                    if await request_controller.check_time(access):
                        test = await request_controller.check_date_quality()
                        print(f"------------ \n {test} \n -------------")
                        await message.answer(return_user_checked(True))

                        opened_loop = Thread(target=user_opened_task)
                        opened_loop.start()
                    else:
                        await message.answer(f" Диапазон от 6 до 23")
                else:
                    await message.answer(return_user_checked(False),
                                         parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())

        case "Открыть 1 уровень":
            access = await request_controller.check_user_on_database()
            if access is not None and access in activate_on_level:
                await message.answer(f"{return_user_checked(True)} 1")
            else:
                await message.answer(return_user_checked(False),
                                     parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())

        case "Открыть 2 уровень":
            access = await request_controller.check_user_on_database()
            if access is not None and access in activate_on_level:
                await message.answer(f"{return_user_checked(user_registered=True)} 2")
            else:
                await message.answer(return_user_checked(False))
        case "Информация о себе":
            user = await get_user(message.from_id)
            await message.answer(
                f"Информация о Вас! \n"
                f"Ваш Telegram ID: <b>{user.id}</b>\n"
                f"ФИО: <b>{user.initials}</b>\n"
                f"Почта: <b>{user.email}</b>\n"
                f"Номер телефона: <b>{user.phoneNumber}</b>\n"
                f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
                f"Уровень: <b>{get_access_level(user.access)}</b>\n",
                parse_mode=types.ParseMode.HTML
            )
            pass
        case "Свободные места":
            pass
        case "Получить ключ":
            pass
    # await state.finish()


def return_user_checked(user_registered: bool) -> str:
    return f"Открыл!" if user_registered else f"Добро пожаловать! \n" \
                                              f"Вы <b>не зарегистрированы</b>." \
                                              f"Пожалуйста, отправьте заявку: <b>/application</b>."


# TODO: Application
@dp.message_handler(Command("application"), state="*")
async def application(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.from_id)
    await message.answer(f"<b>Вы начали подачу заявления</b> \n"
                         f"<b>Введите ФИО: </b>",
                         parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    await ApplicationSubmission.user_fully_name.set()


@dp.message_handler(state=ApplicationSubmission.user_fully_name)
async def application_submission_fully_name(message: types.Message, state: FSMContext):
    await state.update_data(user_fully_name=message.text)
    await message.answer("<b>Введите E-mail: </b>",
                         parse_mode=types.ParseMode.HTML)
    await ApplicationSubmission.user_email.set()


@dp.message_handler(state=ApplicationSubmission.user_email)
async def application_submission_email(message: types.Message, state: FSMContext):
    email_address_re_compile = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if re.search(email_address_re_compile, message.text):
        await state.update_data(user_email=message.text)
        await message.answer("<b>Введите Академическую группу: </b>",
                             parse_mode=types.ParseMode.HTML)
        await ApplicationSubmission.user_academy_group.set()
    else:
        await message.answer("<b>Неправильно введён E-mail.</b> \n"
                             "<b>Например: <strong>prime@example.com</strong></b>", parse_mode=types.ParseMode.HTML)
        return


@dp.message_handler(state=ApplicationSubmission.user_academy_group)
async def application_submission_academy_group(message: types.Message, state: FSMContext):
    await state.update_data(user_academy_group=message.text)
    await message.answer("<b>Введите Государственный номер: </b>"
                         "<b>Например: <strong>А000АА|(регион)</strong></b>",
                         parse_mode=types.ParseMode.HTML)
    await ApplicationSubmission.user_state_number.set()


@dp.message_handler(state=ApplicationSubmission.user_state_number)
async def application_submission_user_state_number(message: types.Message, state: FSMContext):
    state_regex_compiled = re.compile(r"\w\d{3}\w{2}|\d")
    if re.search(state_regex_compiled, message.text.lower()):
        await state.update_data(user_state_number=message.text)
        await message.answer("<b>Данные были отправлены. Ожидайте письма с подтверждением на указанный вами почты.</b>",
                             parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("<b>Неправильно введён государственный номер.</b> \n"
                             "<b>Например: <strong>А000АА|(регион)</strong></b>", parse_mode=types.ParseMode.HTML)
        return
