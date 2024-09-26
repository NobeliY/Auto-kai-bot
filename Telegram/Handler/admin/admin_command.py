from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InputFile

from Data.config import USER_XLSX_PATH
from Handler.admin.change_ap_command import get_change_application
from Keyboard.Inline import delete_menu, show_db_menu
from Keyboard.Inline import main_admin_menu, add_menu, back_inline_menu
from states import Admins
from utils.database_api.quick_commands import get_user, get_users_shortly_info, get_users_info
from utils.database_api.schemas import User, Application
from utils.request_api.Request_controller import RequestController
from utils.shared_methods.default import get_access_level, get_admin_level, get_fully_info


async def call_admin_panel(message: Message):
    if not await get_admin_level(RequestController(message.from_id)):
        return

    user = await get_user(message.from_id)
    await message.answer(f"Добро пожаловать, <b>{user.initials}</b>!",
                         reply_markup=main_admin_menu)
    await Admins.main_state.set()
    await message.delete()


async def users_info(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.show_db_state)
    await query.message.edit_text(f"{await get_users_shortly_info()}",
                                  reply_markup=show_db_menu)


async def set_add_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.add_menu_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=add_menu)


async def set_remove_menu(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.delete_menu_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=delete_menu)


async def show_fully_information(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.show_fully_state)
    await get_fully_info()

    await query.message.delete()
    await query.message.answer_document(InputFile(USER_XLSX_PATH),
                                        reply_markup=back_inline_menu)


async def preview_step(query: CallbackQuery, state: FSMContext):
    state_level = await state.get_state()
    _state_list = {
        'main': [
            "Admins:show_db_state",
            "Admins:add_menu_state",
            "Admins:delete_menu_state",
            "Admins:show_change_application"
        ],
        'add_menu': [
            "Admins:auto_add_state",
            "Admins:manual_add_state"
        ],
        'delete_menu': [
            "Admins:searched_user_delete_state",
            "Admins:delete_all_group_state"
        ],
        'show_db_menu': [
            "Admins:show_fully_state"
        ],
        'show_change_application': [
            "Admins:show_selected_change_application"
        ],
        'change_user_info_state': [
            "Admins:change_user_info_state_by_id",
        ],
    }
    if state_level in _state_list['main']:
        await return_call_admin_panel(query=query, state=state)
    elif state_level in _state_list['add_menu']:
        await set_add_menu(query, state)
    elif state_level in _state_list['delete_menu']:
        await set_remove_menu(query, state)
    elif state_level in _state_list['show_db_menu']:
        await reset_admin_panel(query=query, state=state)
    elif state_level in _state_list['show_change_application']:
        await get_change_application(query=query)


async def return_call_admin_panel(query: CallbackQuery, state: FSMContext):
    user = await get_user(query.message.chat.id)
    await state.set_state(Admins.main_state)
    await query.message.edit_text(f"Добро пожаловать, <b>{user.initials}</b>!",
                                  reply_markup=main_admin_menu)


async def reset_admin_panel(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.main_state)
    user = await get_user(query.message.chat.id)
    await query.message.delete()
    await query.message.answer(f"Добро пожаловать, <b>{user.initials}</b>!",
                               reply_markup=main_admin_menu)


async def build_application_info(application: Application) -> str:
    return f"Информация о пользователе! \n" \
           f"Telegram ID: <b>{application.id}</b>\n" \
           f"ФИО: <b>{application.initials}</b>\n" \
           f"Почта: <b>{application.email}</b>\n" \
           f"Группа: <b>{application.group}</b>\n" \
           f"Номер телефона: <b>{application.phoneNumber}</b>\n" \
           f"Гос. номер используемого транспорта: <b>{application.stateNumber}</b>\n"
