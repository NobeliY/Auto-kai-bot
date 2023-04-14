from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified
from asyncpg import UniqueViolationError

from Handler.admin.admin_command import preview_step
from utils.shared_methods.default import Level, check_initials, check_email, check_phone, check_state_number
from Keyboard.Inline import (
    back_inline_menu,
    add_by_applications_menu,
    application_change_menu,
    application_or_manual_submit_menu,
    application_reject_menu,
    application_approve_level_menu,
    manual_add_menu
)
from Keyboard.Inline import manual_approve_menu
from states import Admins
from states.admins import ManualAdd
from utils.database_api.quick_commands import (
    get_count_of_applications,
    get_all_applications,
    drop_application,
    add_ready_application,
    add_user
)
from utils.database_api.schemas.application import Application

_application_list_ = []
_reversed_application_list_ = []

_linked_query_dict = {}
_manual_user_access_level_dict = {
    'student': 'Студент',
    'student_plus': 'Студент с инвалидностью',
    'teacher': 'Преподаватель',
    'employee': 'Сотрудник',
    'administrator': 'Администратор',
}


async def auto_add_by_application(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admins.auto_add_state)
    count = await get_count_of_applications()
    if not count:
        await query.message.edit_text("Нет заявок!",
                                      reply_markup=back_inline_menu)
        return
    await query.message.edit_text(f"Найдено: <b>{count}</b>\n"
                                  f"Выберите один из вариантов обработки.",
                                  reply_markup=add_by_applications_menu)


async def get_application_from_begin(query: CallbackQuery, state: FSMContext, edit_message: bool = True):
    global _application_list_
    if not _application_list_:
        _application_list_ = await get_all_applications()
    application = await get_elem_from_application_list_()
    if edit_message:
        await query.message.edit_text(await build_application_info(application=application),
                                      reply_markup=application_change_menu)
    await state.update_data({
        'data': application,
        'reversed': False,
    })


async def next_application(query: CallbackQuery, state: FSMContext):
    application_obj = await state.get_data()
    if application_obj['reversed']:
        await insert_elem_from_reversed_application_list_(application_obj['data'])
        await get_application_from_end(query=query, state=state)
        return
    await insert_elem_from_application_list_(application_obj['data'])
    await get_application_from_begin(query=query, state=state)


async def approve_application_from_list(query: CallbackQuery):
    await query.message.edit_reply_markup(application_or_manual_submit_menu)


async def submit_reject_application(query: CallbackQuery, state: FSMContext):
    application_response_dict = await state.get_data()
    await query.message.edit_text(f"Вы уверены, что хотите отклонить заявку:\n"
                                  f"{await build_application_info(application_response_dict['data'])}",
                                  reply_markup=application_reject_menu)


async def reject_application(query: CallbackQuery, state: FSMContext):
    application_response_dict = await state.get_data()
    if await drop_application(application_response_dict['data']):
        await query.message.edit_text(f"Успешно удален:\n"
                                      f"{await build_application_info(application_response_dict['data'])}",
                                      reply_markup=back_inline_menu)
        await state.reset_data()
        await get_application_from_begin(query=query, state=state, edit_message=False) if not application_response_dict[
            'reversed'] else await get_application_from_end(query=query, state=state, edit_message=False)

        return
    await query.message.edit_text(f"Не удалось удалить:\n"
                                  f"{await build_application_info(application_response_dict['data'])}",
                                  reply_markup=back_inline_menu)
    await add_ready_application(application=application_response_dict['data'])
    await insert_elem_from_application_list_(application_response_dict['data']) if not application_response_dict[
        'reversed'] else await insert_elem_from_reversed_application_list_(application_response_dict['data'])


async def get_application_from_end(query: CallbackQuery, state: FSMContext, edit_message: bool = True):
    global _reversed_application_list_
    if not _reversed_application_list_:
        _reversed_application_list_ = list(reversed(await get_all_applications()))
    application = await get_elem_from_reversed_application_list_()
    if edit_message:
        await query.message.edit_text(await build_application_info(application=application),
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


async def approve_student_level_from_application(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(await build_message_approve_level_from_application(state,
                                                                                     level=Level.value(query.data)),
                                  reply_markup=application_approve_level_menu)


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


async def manual_add_user(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.manual_add_state)
    await query.message.edit_text("Вы выбрали ручное добавление пользователя!\n"
                                  "Для того, чтобы начать, нажмите <b>Добавить</b>!\n"
                                  "Для того, чтобы отменить добавление, нажмите <b>Отмена</b>!",
                                  reply_markup=manual_add_menu)


async def start_manual_add(query: CallbackQuery, state: FSMContext):
    print(await state.get_state())
    await ManualAdd.id.set()
    print(await state.get_state())
    global _linked_query_dict
    _linked_query_dict[query.message.chat.id] = query
    await query.message.edit_text("Введите <b>Telegram ID</b>:")


async def get_user_id_from_manual_add(message: Message, state: FSMContext):
    global _linked_query_dict
    query = _linked_query_dict[message.chat.id]
    print(message.chat.id)
    if not message.text.isdigit():
        try:
            await query.message.edit_text("Telegram ID должен содержать только целые числа!")
        except MessageNotModified:
            pass
        await message.delete()
        return
    await state.update_data(id=int(message.text))
    await query.message.edit_text("Введите <b>ФИО</b>:")
    await ManualAdd.initials.set()
    await message.delete()


async def get_user_initials_from_manual_add(message: Message, state: FSMContext) -> None:
    global _linked_query_dict
    query = _linked_query_dict[message.from_id]
    if check_initials(message.text):
        await state.update_data(initials=message.text)
        await query.message.edit_text("Введите <b>E-mail</b>:")
        await ManualAdd.email.set()
        await message.delete()
        return
    try:
        await query.message.edit_text("ФИО должно содержать только Буквы.")
    except MessageNotModified:
        pass
    _linked_query_dict[message.from_id] = query
    await message.delete()


async def get_user_email_from_manual_add(message: Message, state: FSMContext):
    global _linked_query_dict
    query = _linked_query_dict[message.from_id]
    if check_email(message.text):
        await state.update_data(email=message.text)
        await query.message.edit_text("Введите <b>номер телефона: </b>")
        _linked_query_dict[message.from_id] = query
        await ManualAdd.phone_number.set()
        await message.delete()
        return
    try:
        await query.message.edit_text("<b>Неправильно введён E-mail.</b> \n"
                                      "Например: <b>prime@example.com</b>")
    except MessageNotModified:
        pass
    await message.delete()


async def get_user_phone_number_from_manual_add(message: Message, state: FSMContext):
    global _linked_query_dict
    query = _linked_query_dict[message.from_id]
    if check_phone(message.text):
        await state.update_data(phone_number=message.text)
        await query.message.edit_text("Введите <b>Академическую группу</b>:")
        _linked_query_dict[message.from_id] = query
        await message.delete()
        await ManualAdd.academy_group.set()
        return
    try:
        await query.message.edit_text("<b>Неправильно введён номер телефона.</b> \n"
                                      "Например: <b>89999999999</b>")
    except MessageNotModified:
        pass
    await message.delete()
    return


async def get_academy_group_from_manual_add(message: Message, state: FSMContext):
    global _linked_query_dict
    query = _linked_query_dict[message.from_id]
    await state.update_data(group=message.text)
    try:
        await query.message.edit_text("Введите <b>Гос. номер ТС</b>:")
    except MessageNotModified:
        pass
    _linked_query_dict[message.from_id] = query
    await ManualAdd.state_number.set()
    await message.delete()


async def get_user_state_number_from_manual_add(message: Message, state: FSMContext):
    query = _linked_query_dict[message.from_id]
    if check_state_number(message.text):
        await state.update_data(state_number=message.text)
        await query.message.edit_text("Выберите <b>уровень доступа:</b>",
                                      reply_markup=application_or_manual_submit_menu)
        await ManualAdd.level.set()
        await message.delete()
        return
    try:
        await query.message.edit_text("<b>Неправильно введён государственный номер.</b> \n"
                                      "Например: <b>А000АА|(регион)</b>")
    except MessageNotModified:
        pass
    await message.delete()
    _linked_query_dict[message.from_id] = query
    return


async def get_user_access_from_manual_add(query: CallbackQuery, state: FSMContext):
    match query.data:
        case 'student':
            await state.update_data(level='S')
        case 'student_plus':
            await state.update_data(level='I')
        case 'teacher':
            await state.update_data(level='T')
        case 'employee':
            await state.update_data(level='E')
        case 'administrator':
            await state.update_data(level='A')

    user = await state.get_data()

    await query.message.edit_text(f"Вы уверены, что хотите добавить:\n"
                                  f"Telegram ID: <b>{user['id']}</b>\n"
                                  f"ФИО: <b>{user['initials']}</b>\n"
                                  f"Почта: <b>{user['email']}</b>\n"
                                  f"Группа: <b>{user['group']}</b>\n"
                                  f"Гос. номер используемого транспорта: <b>{user['state_number']}</b>\n"
                                  f"Уровень: <b>{_manual_user_access_level_dict[query.data]}</b>\n",
                                  reply_markup=manual_approve_menu)
    await ManualAdd.approve.set()


async def approve_manual_add_user(query: CallbackQuery, state: FSMContext):
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
        await query.message.edit_text("Успешно добавлен",
                                      reply_markup=back_inline_menu)

    except UniqueViolationError:
        await query.message.edit_text(f"Данный пользователь уже существует!",
                                      reply_markup=back_inline_menu)

    await state.reset_data()
    await Admins.manual_add_state.set()


async def cancel_manual_add(query, state: FSMContext):
    if query is CallbackQuery:
        await Admins.manual_add_state.set()
        await preview_step(query, state)
        global _linked_query_dict
        del _linked_query_dict[query.message.chat.id]
