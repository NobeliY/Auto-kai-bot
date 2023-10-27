import logging as logger
from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageNotModified
from colorama import Fore

from Keyboard.Inline import change_info_menu, change_info_list_menu
from Keyboard.Inline.user_keyboard import accept_changes_menu, close_inline_keyboard, preview_step_menu
from Handler.default.start_command import get_admins_id_list
from utils.shared_methods.default import send_user_application_info
from app import bot
from states import UserChanges, UserState

from utils.database_api.quick_commands import get_user, add_application
from utils.shared_methods.default import soon_info, get_access_level, check_initials, check_email, check_phone, \
    check_state_number


async def preview_step(query: CallbackQuery, state: FSMContext) -> None:
    state_level = await state.get_state()
    if state_level in ["UserChanges:change_menu"]:
        await UserState.in_active.set()
        await get_user_info(message=query.message, sec=query.from_user.id)


async def get_user_info(message: Message, sec: int = -1) -> None:
    if sec < 0:
        user = await get_user(message.from_id)
    else:
        user = await get_user(sec)
    await message.answer(
        f"Информация о Вас! \n"
        f"Ваш Telegram ID: <b>{user.id}</b>\n"
        f"ФИО: <b>{user.initials}</b>\n"
        f"Почта: <b>{user.email}</b>\n"
        f"Номер телефона: <b>{user.phoneNumber}</b>\n"
        f"Модель автомобиля: <b>{user.car_mark}</b>\n"
        f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
        f"Уровень: <b>{get_access_level(user.access)}</b>\n",
        reply_markup=change_info_menu
    )
    await message.delete()


async def close_user_info(query: CallbackQuery, state: FSMContext) -> None:
    if await state.get_state() is UserState.is_guest:
        await UserState.in_active.set()
    try:
        await query.message.delete()
    except MessageToDeleteNotFound:
        logger.error(f"{Fore.LIGHTRED_EX}{query.message.from_id} | Try delete message with close info.")


async def change_user_info(query: CallbackQuery, state: FSMContext) -> None:
    await set_user_info_change(query.message, state)
    await state.update_data(user_id=int(query.from_user.id))


async def set_user_info_change(message: Message, state: FSMContext, sec: bool = False) -> None:
    await UserChanges.change_menu.set()
    await state.update_data(chat_id=message.chat.id)
    try:
        text: str = f"Выберите пункт (Несколько), который хотите изменить:\n"
        if not sec:
            await message.answer(text, reply_markup=change_info_list_menu)
        else:
            await message.edit_text(text, reply_markup=preview_step_menu)
        await message.delete()
    except MessageNotModified:
        pass
    except MessageToDeleteNotFound:
        pass


async def send_change_text(message: Message, state: str) -> None:
    try:
        await message.edit_text(f"Введите {state}",
                                reply_markup=preview_step_menu)
    except MessageNotModified:
        pass


async def change_initials(query: CallbackQuery, state: FSMContext) -> None:
    await UserChanges.change_initials.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text(message=query.message, state="ФИО")


async def get_change_initials(message: Message, state: FSMContext) -> None:
    if check_initials(message.text):
        await state.update_data(change_initials=message.text)
        await set_user_info_change(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>ФИО</b> должно содержать только Буквы.",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=preview_step_menu)
        await message.delete()
    except MessageNotModified | MessageToDeleteNotFound:
        pass


async def change_email(query: CallbackQuery, state: FSMContext) -> None:
    await UserChanges.change_email.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text(message=query.message, state="E-mail")


async def get_change_email(message: Message, state: FSMContext) -> None:
    if check_email(message.text):
        await state.update_data(change_email=message.text)
        await set_user_info_change(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>Неправильно введён E-mail.</b> \n"
                                         "Например: <b>prime@example.com</b>",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=preview_step_menu)
        await message.delete()
    except MessageNotModified | MessageToDeleteNotFound:
        pass


async def change_phone_number(query: CallbackQuery, state: FSMContext) -> None:
    await UserChanges.change_phone.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text(message=query.message, state="номер телефона")


async def get_change_phone(message: Message, state: FSMContext) -> None:
    if check_phone(message.text):
        await state.update_data(change_phone=message.text)
        await set_user_info_change(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>Неправильно введён номер телефона.</b> \n"
                                         "Например: <b>89999999999</b>",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=preview_step_menu)
        await message.delete()
    except MessageNotModified | MessageToDeleteNotFound:
        pass


async def change_group(query: CallbackQuery, state: FSMContext) -> None:
    await UserChanges.change_group.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text(message=query.message, state="академическую группу")


async def get_change_group(message: Message, state: FSMContext) -> None:
    await state.update_data(change_group=message.text)
    await set_user_info_change(message=message, state=state)


async def change_car_mark(query: CallbackQuery, state: FSMContext):
    await UserChanges.change_car_mark.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text(message=query.message, state="<b>модель автомобиля</b>")

async def get_change_car_mark(message: Message, state: FSMContext):
    await state.update_data(change_car_mark=message.text)
    await set_user_info_change(message=message, state=state)


async def change_state_number(query: CallbackQuery, state: FSMContext) -> None:
    await UserChanges.change_state_number.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text(message=query.message, state="гос. номер")


async def get_change_state_number(message: Message, state: FSMContext) -> None:
    if check_state_number(message.text):
        await state.update_data(change_state_number=message.text)
        await set_user_info_change(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>Неправильно введён государственный номер.</b> \n"
                                         "Например: <b>А000АА|(регион)</b>",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=preview_step_menu)
        await message.delete()
    except MessageNotModified:
        pass
    except MessageToDeleteNotFound:
        pass


async def accept_changes(query: CallbackQuery, state: FSMContext) -> None:
    data: dict = await state.get_data()
    print(data)
    states_list: List[str] = [
        'change_initials',
        'change_email',
        'change_phone',
        'change_group',
        'change_car_mark',
        'change_state_number'
    ]
    for key in states_list:
        if key not in data.keys():
            data[key] = 'без изменений'

    await state.update_data({
        'user_id': data['user_id'],
        'change_initials': data['change_initials'],
        'change_email': data['change_email'],
        'change_phone': data['change_phone'],
        'change_group': data['change_group'],
        'change_car_mark': data['change_car_mark'],
        'change_state_number': data['change_state_number']
    })
    try:
        await query.message.edit_text(f"Вы точно хотите изменить данные на: \n"
                                      f"ФИО: {data['change_initials']}\n"
                                      f"Почта: {data['change_email']}\n"
                                      f"Номер телефона: {data['change_phone']}\n"
                                      f"Академическая группа: {data['change_group']}\n"
                                      f"Модель ТС: {data['change_car_mark']}\n"
                                      f"Гос. номер: {data['change_state_number']}",
                                      reply_markup=accept_changes_menu)
    except MessageNotModified:
        pass


async def agree_changes(query: CallbackQuery, state: FSMContext) -> None:
    _application = await state.get_data()
    print(_application)

    states_list: List[str] = [
        'change_initials',
        'change_email',
        'change_phone',
        'change_group',
        'change_state_number'
    ]
    for key in states_list:
        if _application[key] == 'без изменений':
            _application[key] = ''
    await add_application(
        user_id=_application['user_id'],
        initials=_application['change_initials'],
        email=_application['change_email'],
        phone_number=_application['change_phone'],
        group=_application['change_group'],
        car_mark=_application["change_car_mark"],
        state_number=_application['change_state_number'],
        change_ap=True
    )
    try:
        await query.message.edit_text(f"Данные отправлены. Ожидайте изменения информации!",
                                      reply_markup=close_inline_keyboard)
        [
                await send_user_application_info(telegram_id=admin_id,
                                                 message=f"Добавлена новая заявка на обновление данных!")
                for admin_id in await get_admins_id_list()
            ]
    except MessageNotModified:
        pass


async def cancel_changes(query: CallbackQuery, state: FSMContext) -> None:
    await preview_step(query=query, state=state)


async def continue_changes(query: CallbackQuery) -> None:
    try:
        await query.message.answer(f"Сохранено! \n"
                                   f"Выберите пункт (Несколько), который хотите изменить:\n",
                                   reply_markup=change_info_list_menu)
    except MessageNotModified:
        pass


async def get_free_positions(message: Message) -> None:
    await message.answer(await soon_info())
    await message.delete()


async def close_info(query: CallbackQuery, state: FSMContext) -> None:
    await UserState.in_active.set()
    try:
        await query.message.delete()
    except MessageToDeleteNotFound:
        await query.message.edit_text("Nothing")
        await query.message.delete()


async def preview_step_info(query: CallbackQuery, state: FSMContext) -> None:
    state_level = await state.get_state()
    _states_list: dict = {
        'change_menu': [
            'UserChanges:change_initials',
            'UserChanges:change_email',
            'UserChanges:change_phone',
            'UserChanges:change_group',
            'UserChanges:change_state_number',
            'UserChanges:accept'
        ]
    }
    if state_level in _states_list['change_menu']:
        await set_user_info_change(query.message, state)