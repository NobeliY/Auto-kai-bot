import csv
from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ParseMode, InputFile

from app import dp
from Data import USER_CSV_PATH, __all_states__
from Handler.default import get_admin_level, get_access_level
from Keyboard.Inline import main_admin_menu, add_menu, back_inline_menu
from Keyboard.Inline import delete_menu, show_db_menu

from states import Admins
from utils.database_api.quick_commands import get_user, get_users_shortly_info, get_users_info
from utils.database_api.schemas.application import Application
from utils.database_api.schemas.user import User
from utils.request_api.Request_controller import RequestController


@dp.message_handler(Text(equals="панель для администратора", ignore_case=True),
                    state=__all_states__)
async def call_admin_panel(message: Message):
    if not await get_admin_level(RequestController(message.from_id)):
        return

    user = await get_user(message.from_id)
    await message.answer(f"Добро пожаловать, <b>{user.initials}</b>!",
                         parse_mode=ParseMode.HTML, reply_markup=main_admin_menu)
    await Admins.main_state.set()
    await message.delete()


@dp.callback_query_handler(Text(equals="users_info"),
                           state=Admins.main_state)
async def users_info(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.show_db_state)
    await query.message.edit_text(f"{await get_users_shortly_info(query.message.chat.id)}",
                                  reply_markup=show_db_menu, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(Text(equals="user_add_menu"),
                           state=Admins.main_state)
async def set_add_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.add_menu_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=add_menu)


@dp.callback_query_handler(Text(equals="user_remove_menu"),
                           state=Admins.main_state)
async def set_remove_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.delete_menu_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=delete_menu)


@dp.callback_query_handler(Text(equals="show_applications"),
                           state=Admins.main_state)
async def show_applications(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.show_applications_state)
    await query.message.edit_text("Происходит доработка",
                                  reply_markup=back_inline_menu)


@dp.callback_query_handler(Text(equals="show_fully_information_from_db"),
                           state=Admins.show_db_state)
async def show_fully_information(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.show_fully_state)
    users: List[User] = await get_users_info(query.message.chat.id)
    fully_info_csv: List[List[str]] = [
        [
            "Telegram ID",
            "ФИО",
            "Почта",
            "Группа",
            "Номер телефона",
            "Гос. номер используемого транспорта",
            "Уровень"
        ]
    ]
    for user in users:
        fully_info_csv.append([
                str(user.id),
                user.initials,
                user.email,
                user.group,
                user.phoneNumber,
                user.stateNumber,
                get_access_level(user.access)
            ])

    with open(USER_CSV_PATH, 'w', encoding='utf-8', newline='') as file:
        csv_file = csv.writer(file)
        csv_file.writerows(fully_info_csv)
    await query.message.delete()
    await query.message.answer_document(InputFile(USER_CSV_PATH),
                                        reply_markup=back_inline_menu)


@dp.callback_query_handler(Text(equals="preview_step"),
                           state=Admins.all_states)
async def preview_step(query: CallbackQuery, state: FSMContext):
    state_level = await state.get_state()
    _state_list = {
        'main': [
            "Admin:show_db_state",
            "Admin:add_menu_state",
            "Admin:delete_menu_state",
            "Admin:show_applications_state"
        ],
        'add_menu': [
            "Admin:auto_add_state",
            "Admin:manual_add_state"
        ],
        'delete_menu': [
            "Admin:searched_user_delete_state",
            "Admin:delete_all_group_state"
        ],
        'show_db_menu': [
            "Admin:show_fully_state"
        ]
    }
    if state_level in _state_list['main']:
        await return_call_admin_panel(query=query, state=state)
    elif state_level in _state_list['add_menu']:
        await set_add_menu(query, state)
    elif state_level in _state_list['delete_menu']:
        await set_remove_menu(query, state)
    elif state_level in _state_list['show_db_menu']:
        await reset_admin_panel(query=query, state=state)


async def return_call_admin_panel(query: CallbackQuery, state: FSMContext):
    user = await get_user(query.message.chat.id)
    await state.set_state(Admins.main_state)
    await query.message.edit_text(f"Добро пожаловать, <b>{user.initials}</b>!",
                                  parse_mode=ParseMode.HTML, reply_markup=main_admin_menu)


async def reset_admin_panel(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.main_state)
    user = await get_user(query.message.chat.id)
    await query.message.delete()
    await query.message.answer(f"Добро пожаловать, <b>{user.initials}</b>!",
                               parse_mode=ParseMode.HTML, reply_markup=main_admin_menu)


async def build_application_info(application: Application) -> str:
    return f"Информация о пользователе! \n" \
           f"Telegram ID: <b>{application.id}</b>\n" \
           f"ФИО: <b>{application.initials}</b>\n" \
           f"Почта: <b>{application.email}</b>\n" \
           f"Группа: <b>{application.group}</b>\n" \
           f"Номер телефона: <b>{application.phoneNumber}</b>\n" \
           f"Гос. номер используемого транспорта: <b>{application.stateNumber}</b>\n"
