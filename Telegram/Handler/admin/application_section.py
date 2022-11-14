from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ParseMode

from Keyboard.Inline import back_inline_menu
from Keyboard.Inline.InlineKeyboard import add_by_applications_menu, application_change_menu, \
    application_submit_menu, application_reject_menu, application_approve_level_menu
from app import dp, bot
from states import Admin
from utils.database_api.quick_commands import get_count_of_applications, get_all_applications, drop_application, \
    add_ready_application, add_user
from utils.database_api.schemas.application import Application

_application_list = []
_reversed_application_list = []


@dp.callback_query_handler(Text(equals="auto_add_by_application"),
                           state=Admin.add_menu_state)
async def auto_add_by_application(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.auto_add_state)
    count = await get_count_of_applications(query.message.chat.id)
    if not count:
        await query.message.edit_text("Нет заявок!",
                                      reply_markup=back_inline_menu)
        return
    await query.message.edit_text(f"Найдено: <b>{count}</b>\n"
                                  f"Выберите один из вариантов обработки.",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=add_by_applications_menu)


@dp.callback_query_handler(Text(equals="start_from_begin"),
                           state=Admin.auto_add_state)
async def get_application_from_begin(query: CallbackQuery, state: FSMContext, edit_message: bool = True):
    global _application_list
    if not _application_list:
        _application_list = await get_all_applications(query.message.chat.id)
    application = await get_elem_from_application_list()
    if edit_message:
        await query.message.edit_text(await build_application_info(application=application),
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=application_change_menu)
    await state.update_data({
        'data': application,
        'reversed': False,
    })


@dp.callback_query_handler(Text(equals="next_application"),
                           state=Admin.auto_add_state)
async def next_application(query: CallbackQuery, state: FSMContext):
    application_obj = await state.get_data()
    if application_obj['reversed']:
        await insert_elem_from_reversed_application_list(application_obj['data'])
        await get_application_from_end(query=query, state=state)
        return
    await insert_elem_from_application_list(application_obj['data'])
    await get_application_from_begin(query=query, state=state)


@dp.callback_query_handler(Text(equals="approve_application"),
                           state=Admin.auto_add_state)
async def approve_application(query: CallbackQuery):
    await query.message.edit_reply_markup(application_submit_menu)


@dp.callback_query_handler(Text(equals="submit_reject_application"),
                           state=Admin.auto_add_state)
async def submit_reject_application(query: CallbackQuery, state: FSMContext):
    application_response_dict = await state.get_data()
    await query.message.edit_text(f"Вы уверены, что хотите отклонить заявку:\n"
                                  f"{await build_application_info(application_response_dict['data'])}",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_reject_menu)


@dp.callback_query_handler(Text(equals="reject_application"),
                           state=Admin.auto_add_state)
async def reject_application(query: CallbackQuery, state: FSMContext):
    application_response_dict = await state.get_data()
    if await drop_application(application_response_dict['data']):
        await query.message.edit_text(f"Успешно удален:\n"
                                      f"{await build_application_info(application_response_dict['data'])}",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=back_inline_menu)
        await state.reset_data()
        await get_application_from_begin(query=query,state=state,edit_message=False) if not application_response_dict[
            'reversed'] else await get_application_from_end(query=query, state=state, edit_message=False)

        return
    await query.message.edit_text(f"Не удалось удалить:\n"
                                  f"{await build_application_info(application_response_dict['data'])}",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=back_inline_menu)
    await add_ready_application(application=application_response_dict['data'])
    await insert_elem_from_application_list(application_response_dict['data']) if not application_response_dict[
        'reversed'] else await insert_elem_from_reversed_application_list(application_response_dict['data'])


@dp.callback_query_handler(Text(equals="start_from_end"),
                           state=Admin.auto_add_state)
async def get_application_from_end(query: CallbackQuery, state: FSMContext, edit_message: bool = True):
    global _reversed_application_list
    if not _reversed_application_list:
        _reversed_application_list = list(reversed(await get_all_applications(query.message.chat.id)))
    application = await get_elem_from_reversed_application_list()
    if edit_message:
        await query.message.edit_text(await build_application_info(application=application),
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=application_change_menu)
    await state.update_data({
        'data': application,
        'reversed': True,
    })


async def get_elem_from_reversed_application_list() -> Application | None:
    global _reversed_application_list
    return _reversed_application_list.pop(0)


async def insert_elem_from_reversed_application_list(elem: Application):
    global _reversed_application_list
    _reversed_application_list.append(elem)


async def get_elem_from_application_list() -> Application | None:
    global _application_list
    return _application_list.pop(0)


async def insert_elem_from_application_list(elem: Application):
    global _application_list
    _application_list.append(elem)


@dp.callback_query_handler(Text(equals="student"),
                           state=Admin.auto_add_state)
async def approve_student_level_from_application(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(await build_message_approve_level_from_application(state, level='S'),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_approve_level_menu)


@dp.callback_query_handler(Text(equals="student_plus"),
                           state=Admin.auto_add_state)
async def approve_student_level_from_application(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(await build_message_approve_level_from_application(state, level='I'),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_approve_level_menu)


@dp.callback_query_handler(Text(equals="teacher"),
                           state=Admin.auto_add_state)
async def approve_student_level_from_application(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(await build_message_approve_level_from_application(state, level='T'),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_approve_level_menu)


@dp.callback_query_handler(Text(equals="employee"),
                           state=Admin.auto_add_state)
async def approve_student_level_from_application(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(await build_message_approve_level_from_application(state, level='P'),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_approve_level_menu)


@dp.callback_query_handler(Text(equals="administrator"),
                           state=Admin.auto_add_state)
async def approve_student_level_from_application(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(await build_message_approve_level_from_application(state, level='A'),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_approve_level_menu)


@dp.callback_query_handler(Text(equals="approve_level_application"),
                           state=Admin.auto_add_state)
async def approve_application(query: CallbackQuery, state: FSMContext):
    application_object: dict = await state.get_data()
    application: Application = application_object['data']
    level: str = application_object['level']
    await add_user(
        user_id=application.id,
        initials=application.initials,
        email=application.email,
        phone_number=application.phoneNumber,
        group=application.group,
        state_number=application.stateNumber,
        access=level
    )
    await query.message.edit_text(f"Успешно добавлен\n"
                                  f"{await build_application_info(application)}",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=back_inline_menu)
    await drop_application(application=application)
    await state.reset_data()


async def build_message_approve_level_from_application(state: FSMContext, level: str):
    application_obj = await state.get_data()
    application = application_obj['data']
    application_obj['level'] = level
    await state.update_data(application_obj)
    return f"Вы уверены, что хотите принять заявку:\n" \
           f"Информация о пользователе! \n" \
           f"{await build_application_info(application)}"


async def build_application_info(application: Application):
    return f"Telegram ID: <b>{application.id}</b>\n" \
           f"ФИО: <b>{application.initials}</b>\n" \
           f"Почта: <b>{application.email}</b>\n" \
           f"Группа: <b>{application.group}</b>\n" \
           f"Номер телефона: <b>{application.phoneNumber}</b>\n" \
           f"Гос. номер используемого транспорта: <b>{application.stateNumber}</b>\n"


@dp.callback_query_handler(Text(equals="manual_add"),
                           state=Admin.add_menu_state)
async def manual_add_user(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.manual_add_state)
    await query.message.edit_text("В разработке",
                                  reply_markup=back_inline_menu)
