from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from Keyboard.Inline import add_by_applications_menu, back_inline_menu, application_change_menu, \
    application_reject_menu, application_approve_menu
from states import Admins
from utils.database_api.quick_commands import get_user, \
    drop_application, add_ready_application, update_user, get_all_applications, get_count_of_applications, \
    get_serialized_application
from utils.database_api.schemas import ApplicationChange

_change_application_list_: List[ApplicationChange] = []
_reversed_change_application_list_: List[ApplicationChange] = []


async def get_change_application(query: CallbackQuery) -> None:
    await Admins.show_change_application.set()
    count = await get_count_of_applications(change_ap=True)
    if not count:
        await query.message.edit_text("Нет заявок!",
                                      reply_markup=back_inline_menu)
        return
    await query.message.edit_text(f"Найдено: <b>{count}</b>\n"
                                  f"Выберите один из вариантов обработки.",
                                  reply_markup=add_by_applications_menu)


async def get_change_application_from_begin(query: CallbackQuery, state: FSMContext, edit_message: bool = True) -> None:
    global _change_application_list_
    if not _change_application_list_:
        _change_application_list_ = await get_all_applications(change_ap=True)
    application = await get_elem_from_change_application_list_()
    if edit_message:
        await query.message.edit_text(await build_change_application_info(application=application),
                                      reply_markup=application_change_menu)
    await state.update_data({
        'data': application.__dict__,
        'reversed': False,
    })


async def next_change_application(query: CallbackQuery, state: FSMContext) -> None:
    application_obj = await state.get_data()
    if application_obj['reversed']:
        await insert_elem_from_reversed_change_application_list_(
            await get_serialized_application(application_obj["data"]["__values__"], True)
        )
        await get_change_application_from_end(query)
        return
    await insert_elem_from_change_application_list_(
        await get_serialized_application(application_obj["data"]["__values__"], True)
    )
    await get_change_application_from_begin(query, state)


async def get_change_application_from_end(query: CallbackQuery, edit_message: bool = True) -> None:
    global _reversed_change_application_list_
    if not _reversed_change_application_list_:
        _reversed_change_application_list_ = list(reversed(await get_all_applications(change_ap=True)))
    application: ApplicationChange | None = await get_elem_from_reversed_change_application_list_()
    if edit_message:
        await query.message.edit_text(await build_change_application_info(application),
                                      reply_markup=application_change_menu)


async def approve_change_application(query: CallbackQuery) -> None:
    await Admins.show_selected_change_application.set()
    await query.message.edit_reply_markup(application_approve_menu)


async def cancel_approve_change_application(query: CallbackQuery, state: FSMContext) -> None:
    application_dict: dict = await state.get_data()
    application = await get_serialized_application(application_dict["data"]["__values__"], True)
    await insert_elem_from_reversed_change_application_list_(
        application) if application_dict['reversed'] else await insert_elem_from_change_application_list_(
        application
    )
    await get_change_application(query)


async def confirm_approve_change_application(query: CallbackQuery, state: FSMContext) -> None:
    application_dict: dict = await state.get_data()
    application = await get_serialized_application(application_dict["data"]["__values__"], True)
    _successful: bool = await update_user(application)
    if _successful:
        try:
            await query.message.edit_text("Успешно обновлены данные!", reply_markup=back_inline_menu)
            await drop_application(application)
        except MessageNotModified:
            pass


async def reject_change_application(query: CallbackQuery, state: FSMContext) -> None:
    application_dict = await state.get_data()
    application = await get_serialized_application(application_dict["data"]["__values__"], True)
    await query.message.edit_text(f"Вы уверены, что хотите отклонить заявку на изменение?\n"
                                  f"{await build_change_application_info(application)}",
                                  reply_markup=application_reject_menu)


async def confirm_reject(query: CallbackQuery, state: FSMContext) -> None:
    application_dict = await state.get_data()
    application = await get_serialized_application(application_dict["data"]["__values__"], True)
    if await drop_application(application):
        await query.message.edit_text(f"Успешно удален:\n"
                                      f"{await build_change_application_info(application)}",
                                      reply_markup=back_inline_menu)
        await state.reset_data()
        await get_change_application_from_begin(query, state, False) if not application_dict[
            'reversed'] else await get_change_application_from_end(query, False)
        return

    await query.message.edit_text(f"Не удалось удалить:\n"
                                  f"{await build_change_application_info(application)}",
                                  reply_markup=back_inline_menu)
    await add_ready_application(application)
    await insert_elem_from_change_application_list_(application) if not application_dict[
        'reversed'] else await insert_elem_from_reversed_change_application_list_(application)


async def insert_elem_from_reversed_change_application_list_(elem: ApplicationChange) -> None:
    global _reversed_change_application_list_
    _reversed_change_application_list_.append(elem)


async def insert_elem_from_change_application_list_(elem: ApplicationChange) -> None:
    global _change_application_list_
    _change_application_list_.append(elem)


async def build_change_application_info(application: ApplicationChange):
    user_ = await get_user(application.id)
    return f"Заявка для изменения данных:\n" \
           f"От: <b>{user_.initials}</b> (<b>{user_.group}</b>)" \
           f"Telegram ID: <b>{application.id}</b>\n" \
           f"ФИО: <b>{application.initials}</b>\n" \
           f"Почта: <b>{application.email}</b>\n" \
           f"Группа: <b>{application.group}</b>\n" \
           f"Номер телефона: <b>{application.phoneNumber}</b>\n" \
           f"Модель автомобиля: <b>{application.car_mark}</b>\n" \
           f"Гос. номер используемого транспорта: <b>{application.stateNumber}</b>\n"


async def get_elem_from_change_application_list_() -> ApplicationChange | None:
    global _change_application_list_
    try:
        return _change_application_list_.pop(0)
    except IndexError:
        return


async def get_elem_from_reversed_change_application_list_() -> ApplicationChange | None:
    global _reversed_change_application_list_
    try:
        return _reversed_change_application_list_.pop(0)
    except IndexError:
        return


async def close_change_application() -> None:
    ...
