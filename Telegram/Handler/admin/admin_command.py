import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ParseMode

from Handler.default import get_admin_level
from Keyboard.Inline import main_admin_menu, add_menu
from Keyboard.Inline.InlineKeyboard import delete_menu, show_db_menu
from app import dp, bot
from states import UserState, Admin
from utils.database_api.quick_commands import get_user, get_users_shortly_info
from utils.request_api.Request_controller import RequestController


@dp.message_handler(Text(equals="панель для администратора", ignore_case=True),
                    state=UserState.all_states or Admin.main_state)
async def call_admin_panel(message: Message, state: FSMContext):
    if not await get_admin_level(RequestController(message.from_id)):
        return

    user = await get_user(message.from_id)
    await message.answer(f"Добро пожаловать, <b>{user.initials}</b>!",
                         parse_mode=ParseMode.HTML, reply_markup=main_admin_menu)
    await Admin.main_state.set()


@dp.callback_query_handler(Text(equals="users_info", ignore_case=True),
                           state=Admin.main_state)
async def users_info(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.show_db_state)
    await query.message.edit_text(f"{await get_users_shortly_info(query.message.chat.id)}",
                                  reply_markup=show_db_menu, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(Text(equals="user_add_menu", ignore_case=True),
                           state=Admin.main_state)
async def set_add_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.add_menu_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=add_menu)


@dp.callback_query_handler(Text(equals="user_remove_menu", ignore_case=True),
                           state=Admin.main_state)
async def set_remove_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.delete_menu_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=delete_menu)


@dp.callback_query_handler(Text(equals="show_applications", ignore_case=True),
                           state=Admin.main_state)
async def show_applications(query: CallbackQuery):
    pass


# TODO Add Menu
@dp.callback_query_handler(Text(equals="auto_add_by_application", ignore_case=True),
                           state=Admin.auto_add_state)
async def auto_add_by_application(query: CallbackQuery):
    pass


@dp.callback_query_handler(Text(equals="manual_add", ignore_case=True),
                           state=Admin.manual_add_state)
async def manual_add_user(query: CallbackQuery):
    pass


# TODO Remove Menu
@dp.callback_query_handler(Text(equals="delete_by_initials", ignore_case=True),
                           state=Admin.main_state)
async def delete_user_by_initials(query: CallbackQuery):
    pass


@dp.callback_query_handler(Text(equals="delete_all_group", ignore_case=True),
                           state=Admin.main_state)
async def delete_all_from_group(query: CallbackQuery):
    pass


@dp.callback_query_handler(Text(equals="preview_step", ignore_case=True),
                           state=Admin.all_states)
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
        ]
    }
    if state_level in _state_list['main']:
        await return_call_admin_panel(query=query, state=state)
    elif state_level in _state_list['add_menu']:
        await set_add_menu(query, state)
    elif state_level in _state_list['delete_menu']:
        await set_remove_menu(query, state)


async def return_call_admin_panel(query: CallbackQuery, state: FSMContext):
    user = await get_user(query.message.chat.id)
    await state.set_state(Admin.main_state)
    await query.message.edit_text(f"Добро пожаловать, <b>{user.initials}</b>!",
                                  parse_mode=ParseMode.HTML, reply_markup=main_admin_menu)



