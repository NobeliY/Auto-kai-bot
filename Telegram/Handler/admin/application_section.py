import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ParseMode, Message
from aiogram.utils.exceptions import MessageNotModified
from asyncpg import UniqueViolationError

from Handler.admin.admin_command import preview_step
from Keyboard.Inline import back_inline_menu, add_by_applications_menu, application_change_menu, \
    application_or_manual_submit_menu, application_reject_menu, application_approve_level_menu, manual_add_menu, \
    cancel_manual_add_menu
from app import dp, bot
from states import Admin
from states.admin import ManualAdd
from utils.database_api.quick_commands import get_count_of_applications, get_all_applications, drop_application, \
    add_ready_application, add_user
from utils.database_api.schemas.application import Application

_application_list_ = []
_reversed_application_list_ = []

_linked_query = {}


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
    global _application_list_
    if not _application_list_:
        _application_list_ = await get_all_applications(query.message.chat.id)
    application = await get_elem_from_application_list_()
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
        await insert_elem_from_reversed_application_list_(application_obj['data'])
        await get_application_from_end(query=query, state=state)
        return
    await insert_elem_from_application_list_(application_obj['data'])
    await get_application_from_begin(query=query, state=state)


@dp.callback_query_handler(Text(equals="approve_application"),
                           state=Admin.auto_add_state)
async def approve_application(query: CallbackQuery):
    await query.message.edit_reply_markup(application_or_manual_submit_menu)


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
        await get_application_from_begin(query=query, state=state, edit_message=False) if not application_response_dict[
            'reversed'] else await get_application_from_end(query=query, state=state, edit_message=False)

        return
    await query.message.edit_text(f"Не удалось удалить:\n"
                                  f"{await build_application_info(application_response_dict['data'])}",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=back_inline_menu)
    await add_ready_application(application=application_response_dict['data'])
    await insert_elem_from_application_list_(application_response_dict['data']) if not application_response_dict[
        'reversed'] else await insert_elem_from_reversed_application_list_(application_response_dict['data'])


@dp.callback_query_handler(Text(equals="start_from_end"),
                           state=Admin.auto_add_state)
async def get_application_from_end(query: CallbackQuery, state: FSMContext, edit_message: bool = True):
    global _reversed_application_list_
    if not _reversed_application_list_:
        _reversed_application_list_ = list(reversed(await get_all_applications(query.message.chat.id)))
    application = await get_elem_from_reversed_application_list_()
    if edit_message:
        await query.message.edit_text(await build_application_info(application=application),
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=application_change_menu)
    await state.update_data({
        'data': application,
        'reversed': True,
    })


async def get_elem_from_reversed_application_list_() -> Application | None:
    global _reversed_application_list_
    try:
        return _reversed_application_list_.pop(0)
    except IndexError:
        return None


async def insert_elem_from_reversed_application_list_(elem: Application):
    global _reversed_application_list_
    _reversed_application_list_.append(elem)


async def get_elem_from_application_list_() -> Application | None:
    global _application_list_
    try:
        return _application_list_.pop(0)
    except IndexError:
        return None


async def insert_elem_from_application_list_(elem: Application):
    global _application_list_
    _application_list_.append(elem)


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
    await query.message.edit_text("Вы выбрали ручное добавление пользователя!\n"
                                  "Для того, чтобы начать, нажмите <b>Добавить</b>!\n"
                                  "Для того, чтобы отменить добавление, нажмите <b>Отмена</b>!",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=manual_add_menu)


@dp.callback_query_handler(Text(equals="start_manual_add"),
                           state=Admin.manual_add_state)
async def start_manual_add(query: CallbackQuery):
    await ManualAdd.id.set()
    global _linked_query
    _linked_query[query.message.chat.id] = query
    await query.message.edit_text("Введите <b>Telegram ID</b>:",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=cancel_manual_add_menu)


@dp.message_handler(state=ManualAdd.id)
async def get_user_id_from_manual_add(message: Message, state: FSMContext):
    global _linked_query
    query = _linked_query[message.from_id]

    if not message.text.isdigit():
        try:
            await query.message.edit_text("Telegram ID должен содержать только целые числа!",
                                          reply_markup=cancel_manual_add_menu)
        except MessageNotModified:
            pass
        await message.delete()
        return
    await state.update_data(id=int(message.text))
    await query.message.edit_text("Введите <b>ФИО</b>:",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=cancel_manual_add_menu)
    await ManualAdd.initials.set()
    await message.delete()


@dp.message_handler(state=ManualAdd.initials)
async def get_user_initials_from_manual_add(message: Message, state: FSMContext):
    global _linked_query
    query = _linked_query[message.from_id]
    if not re.fullmatch(r"^[A-Za-z]+", message.text):
        try:
            await query.message.edit_text("ФИО должно содержать только Буквы.",
                                          reply_markup=cancel_manual_add_menu)
        except MessageNotModified:
            pass
        _linked_query[message.from_id] = query
        await message.delete()
        return
    await state.update_data(initials=message.text)
    await query.message.edit_text("Введите <b>E-mail</b>:",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=cancel_manual_add_menu)
    await ManualAdd.email.set()
    await message.delete()


@dp.message_handler(state=ManualAdd.email)
async def get_user_email_from_manual_add(message: Message, state: FSMContext):
    global _linked_query
    query = _linked_query[message.from_id]
    if re.search(r"[^@]+@[^@]+\.[^@]+", message.text):
        await state.update_data(email=message.text)
        await query.message.edit_text("Введите <b>номер телефона: </b>",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=cancel_manual_add_menu)
        _linked_query[message.from_id] = query
        await ManualAdd.phone_number.set()
        await message.delete()
    else:
        try:
            await query.message.edit_text("<b>Неправильно введён E-mail.</b> \n"
                                          "Например: <b>prime@example.com</b>",
                                          parse_mode=ParseMode.HTML,
                                          reply_markup=cancel_manual_add_menu)
        except MessageNotModified:
            pass
        await message.delete()
        return


@dp.message_handler(state=ManualAdd.phone_number)
async def get_user_phone_number_from_manual_add(message: Message, state: FSMContext):
    global _linked_query
    query = _linked_query[message.from_id]
    if re.fullmatch(r"\d{11}", message.text):
        await state.update_data(phone_number=message.text)
        await query.message.edit_text("Введите <b>Академическую группу</b>:",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=cancel_manual_add_menu)
        _linked_query[message.from_id] = query
        await message.delete()
        await ManualAdd.academy_group.set()
    else:
        try:
            await query.message.edit_text("<b>Неправильно введён номер телефона.</b> \n"
                                          "Например: <b>89999999999</b>",
                                          parse_mode=ParseMode.HTML,
                                          reply_markup=cancel_manual_add_menu)
        except MessageNotModified:
            pass
        await message.delete()
        return


@dp.message_handler(state=ManualAdd.academy_group)
async def get_academy_group_from_manual_add(message: Message, state: FSMContext):
    global _linked_query
    query = _linked_query[message.from_id]
    await state.update_data(group=message.text)
    try:
        await query.message.edit_text("Введите <b>Гос. номер ТС</b>:",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=cancel_manual_add_menu)
    except MessageNotModified:
        pass
    _linked_query[message.from_id] = query
    await ManualAdd.state_number.set()
    await message.delete()


@dp.message_handler(state=ManualAdd.state_number)
async def get_user_state_number_from_manual_add(message: Message, state: FSMContext):
    query = _linked_query[message.from_id]
    if not re.search(r"\w\d{3}\w{2}\|\d", message.text):
        try:
            await query.message.edit_text("<b>Неправильно введён государственный номер.</b> \n"
                                          "Например: <b>А000АА|(регион)</b>",
                                          parse_mode=ParseMode.HTML,
                                          reply_markup=cancel_manual_add_menu)
        except MessageNotModified:
            pass
        await message.delete()
        _linked_query[message.from_id] = query
        return
    await state.update_data(state_number=message.text)
    await query.message.edit_text("Выберите <b>уровень доступа:</b>",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=application_or_manual_submit_menu)


@dp.callback_query_handler(Text(equals="student"),
                           state=ManualAdd.state_number)
@dp.callback_query_handler(Text(equals="student_plus"),
                           state=ManualAdd.state_number)
@dp.callback_query_handler(Text(equals="teacher"),
                           state=ManualAdd.state_number)
@dp.callback_query_handler(Text(equals="employee"),
                           state=ManualAdd.state_number)
@dp.callback_query_handler(Text(equals="administrator"),
                           state=ManualAdd.state_number)
async def get_user_access_from_manual_add(query: CallbackQuery, state: FSMContext):
    print("Catched")
    print(query.data)
    if query.data == 'student':
        await state.update_data(level='S')
    elif query.data == 'student_plus':
        await state.update_data(level='I')
    elif query.data == 'teacher':
        await state.update_data(level='T')
    elif query.data == 'employee':
        await state.update_data(level='E')
    elif query.data == 'administrator':
        await state.update_data(level='A')
    user = await state.get_data()
    try:
        await add_user(
            user_id=user['id'],
            initials=user['initials'],
            email=user['email'],
            phone_number=user['phone_number'],
            group=user['group'],
            state_number=user['state_number'],
            access=user['level']
        )
        print("Created!")
        await query.message.edit_text("Успешно добавлен",
                                      reply_markup=back_inline_menu)

    except UniqueViolationError:
        await query.message.edit_text(f"Данный пользователь уже существует!",
                                      reply_markup=back_inline_menu)
    await state.reset_data()
    await Admin.manual_add_state.set()


@dp.callback_query_handler(Text(equals="cancel_manual_add"),
                           state=ManualAdd.all_states)
async def cancel_manual_add(query: CallbackQuery, state: FSMContext):
    await state.reset_data()
    await Admin.manual_add_state.set()
    await preview_step(query, state)
    global _linked_query
    del _linked_query[query.message.chat.id]
