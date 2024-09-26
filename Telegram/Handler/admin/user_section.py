import logging as logger
from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from colorama import Fore
from aiogram.utils.exceptions import MessageToDeleteNotFound, ChatNotFound, UserDeactivated, MessageNotModified

from Handler.admin.admin_command import preview_step
from Handler.default.start_command import get_admins_id_list
from Keyboard.Inline.admin_change_user_info_keyboard import main_change_user_info_menu, select_searched_user_button, \
    change_info_list_menu_admin, select_accept_menu, change_user_info_preview_step
from app import bot
from states.admins import UserChangesForAdmin
from utils.shared_methods.default import get_access_level, user_to_str, check_initials, check_email, check_phone, \
    check_state_number
from Keyboard.Inline import back_inline_menu, change_info_list_menu
from Keyboard.Inline import delete_accept_menu, delete_fully_show_searched_menu, \
    delete_searched_user_button
from states import Admins
from utils.database_api.quick_commands import delete_users_by_group, get_users_by_group, get_users_by_initials, \
    delete_user_by_initials_command, get_serialized_user, get_user_by_id, get_users_by_phone_number, \
    get_users_by_car_mark, get_user_by_state_number, get_serialized_application, update_user
from utils.database_api.schemas import User


async def delete_user_by_initials(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.searched_user_delete_state)
    await query.message.answer("Введите ФИО (Можно Фамилию имя). \n"
                               "Рекомендуется вводить ФИО полностью")


async def delete_user_by_initials_searched(message: Message, state: FSMContext) -> None:
    users = await get_users_by_initials(initials=message.text)
    if not users:
        await message.answer("Нет пользователя с такими ФИО.", reply_markup=back_inline_menu)
        return
    if len(users) == 1:
        user = users[-1]
        await message.answer(f"Вы точно хотите удалить: \n"
                             f"{await user_to_str(user)}?",
                             reply_markup=delete_accept_menu)
        await state.update_data(data={
            "data": user.__dict__,
        })
        return
    await message.answer(f"По вашему запросу найдено: <b>{len(users)}</b>\n"
                         f"Нажмите на `Подробнее` и выберите из сообщений необходимый!",
                         reply_markup=delete_fully_show_searched_menu)
    await state.update_data(data={
        "data": [user.__dict__ for user in users]
    })


async def send_all_searched_users_for_delete(query: CallbackQuery, state: FSMContext):
    users = await state.get_data()
    for _user in users["data"]:
        user = await get_serialized_user(user_dict=_user["__values__"])
        await query.message.answer(await user_to_str(user),
                                   reply_markup=delete_searched_user_button)


async def delete_user_question(query: CallbackQuery, state: FSMContext):
    initials = query.message.text.split("`")[1]
    try:
        await query.message.delete()
    except Exception as ex_:
        logger.error(f"{Fore.LIGHTRED_EX}{ex_}{Fore.RESET}")
        await query.message.edit_text("Ничего нет!")
    await query.message.answer(f"Вы точно хотите удалить: {initials}",
                               reply_markup=delete_accept_menu)
    users = await get_users_by_initials(initials=initials)
    required_user = users[0]
    await state.update_data(data={
        "data": required_user.__dict__
    })


async def delete_user(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user = await get_serialized_user(user_dict=user_data["data"]["__values__"])
    await delete_user_by_initials_command(user=user)
    await query.message.edit_text(f"Успешно удален: {user.initials}"
                                  ,
                                  reply_markup=back_inline_menu)


async def decline_delete_user(query: CallbackQuery):
    await decline_delete(query)


async def delete_all_from_group(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.delete_all_group_state)
    await query.message.answer("Введите группу для удаления!")


async def get_group_for_delete(message: Message, state: FSMContext):
    users: List[User] | None = await get_users_by_group(group=message.text)
    if not users:
        await message.answer("Нет такой группы в БД.", reply_markup=back_inline_menu)
        return
    await message.answer(f"Найдено: <b>{len(users)}</b>\n"
                         f"Вы точно хотите удалить эту группу?",
                         reply_markup=delete_accept_menu)
    await state.update_data(data={
        "data": [user.__dict__ for user in users]
    })


async def accept_delete_group(query: CallbackQuery, state: FSMContext):
    users = await state.get_data()
    __users__: List[User] = [await get_serialized_user(user["__values__"]) for user in users["data"]]
    await delete_users_by_group(users=__users__)
    await query.message.edit_text(f"Успешна удалена группа: {query.message.text}",
                                  reply_markup=back_inline_menu)


async def decline_delete_group(query: CallbackQuery):
    await decline_delete(query)


async def decline_delete(query: CallbackQuery):
    await query.message.edit_text("<b>Операция отменена!</b>",
                                  reply_markup=back_inline_menu)


'''
Change user info section
'''


async def show_change_user_info_panel(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.change_user_info_state)
    await query.message.edit_text(F"Выберите режим", reply_markup=main_change_user_info_menu)


async def change_user_info_by_id(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.change_user_info_state_by_id)
    await query.message.edit_text(F"Введите ID пользователя!", reply_markup=back_inline_menu)


async def get_user_by_id_for_change(message: Message, state: FSMContext):
    try:
        user = await get_user_by_id(user_id=int(message.text))
    except Exception as ex:
        logger.error(f"{Fore.LIGHTRED_EX}{ex}{Fore.RESET}")
    if not user:
        await message.answer("Нет такого пользователя.", reply_markup=back_inline_menu)
        return
    await state.set_state(UserChangesForAdmin.change_menu_for_admin)
    await state.update_data(data={
        "data": user.__dict__
    })
    await get_user_info_for_admin(message, state)


async def get_user_info_for_admin(message: Message, state: FSMContext) -> None:
    user_ = await state.get_data()
    await state.set_state(UserChangesForAdmin.user_id_for_admin)
    user = await get_serialized_user(user_dict=user_["data"]["__values__"])
    await message.answer(
        f"Информация о Пользователе! \n"
        f"Telegram ID: <b>{user.id}</b>\n"
        f"ФИО: <b>{user.initials}</b>\n"
        f"Академическая группа: <b>{user.group}</b>\n"
        f"Почта: <b>{user.email}</b>\n"
        f"Номер телефона: <b>{user.phoneNumber}</b>\n"
        f"Модель автомобиля: <b>{user.car_mark}</b>\n"
        f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
        f"Уровень: <b>{get_access_level(user.access)}</b>\n",
        reply_markup=select_searched_user_button
    )
    await message.delete()


async def close_user_info_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    if await state.get_state() is UserChangesForAdmin.user_id_for_admin:
        await Admins.change_user_info_state.set()
    try:
        await query.message.delete()
    except MessageToDeleteNotFound:
        logger.error(f"{Fore.LIGHTRED_EX}{query.message.from_id} | Try delete message with close info.")


async def change_user_info(query: CallbackQuery, state: FSMContext) -> None:
    await set_user_info_change_for_admin(query.message, state)
    # await state.update_data(user_id=int(query.from_user.id))


async def set_user_info_change_for_admin(message: Message, state: FSMContext) -> None:
    user_ = await state.get_data()
    user = await get_serialized_user(user_dict=user_["data"]["__values__"])
    await UserChangesForAdmin.change_menu_for_admin.set()
    await state.update_data(chat_id=user.id)
    try:
        text: str = f"Выберите пункт (Несколько), который хотите изменить:\n"
        await message.answer(text, reply_markup=change_info_list_menu_admin)
        await message.delete()
    except MessageNotModified:
        pass
    except MessageToDeleteNotFound:
        pass


async def send_change_text_for_admin(message: Message, state: str) -> None:
    try:
        await message.edit_text(f"Введите {state}",
                                reply_markup=change_user_info_preview_step)
    except MessageNotModified:
        pass


async def change_initials_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    await UserChangesForAdmin.change_initials_for_admin.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text_for_admin(message=query.message, state="ФИО")


async def get_change_initials_for_admin(message: Message, state: FSMContext) -> None:
    if check_initials(message.text):
        await state.update_data(change_initials=message.text)
        await set_user_info_change_for_admin(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>ФИО</b> должно содержать только Буквы.",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=change_user_info_preview_step)
        await message.delete()
    except MessageNotModified | MessageToDeleteNotFound:
        pass


async def change_email_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    await UserChangesForAdmin.change_email_for_admin.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text_for_admin(message=query.message, state="E-mail")


async def get_change_email_for_admin(message: Message, state: FSMContext) -> None:
    if check_email(message.text):
        await state.update_data(change_email=message.text)
        await set_user_info_change_for_admin(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>Неправильно введён E-mail.</b> \n"
                                         "Например: <b>prime@example.com</b>",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=change_user_info_preview_step)
        await message.delete()
    except MessageNotModified | MessageToDeleteNotFound:
        pass


async def change_phone_number_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    await UserChangesForAdmin.change_phone_for_admin.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text_for_admin(message=query.message, state="номер телефона")


async def get_change_phone_for_admin(message: Message, state: FSMContext) -> None:
    if check_phone(message.text):
        await state.update_data(change_phone=message.text)
        await set_user_info_change_for_admin(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>Неправильно введён номер телефона.</b> \n"
                                         "Например: <b>89999999999</b>",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=change_user_info_preview_step)
        await message.delete()
    except MessageNotModified | MessageToDeleteNotFound:
        pass


async def change_group_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    await UserChangesForAdmin.change_group_for_admin.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text_for_admin(message=query.message, state="академическую группу")


async def get_change_group_for_admin(message: Message, state: FSMContext) -> None:
    await state.update_data(change_group=message.text)
    await set_user_info_change_for_admin(message=message, state=state)


async def change_car_mark_for_admin(query: CallbackQuery, state: FSMContext):
    await UserChangesForAdmin.change_car_mark_for_admin.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text_for_admin(message=query.message, state="<b>модель автомобиля</b>")


async def get_change_car_mark_for_admin(message: Message, state: FSMContext):
    await state.update_data(change_car_mark=message.text)
    await set_user_info_change_for_admin(message=message, state=state)


async def change_state_number_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    await UserChangesForAdmin.change_state_number_for_admin.set()
    await state.update_data(behind_message=query.message.message_id)
    await send_change_text_for_admin(message=query.message, state="гос. номер")


async def get_change_state_number_for_admin(message: Message, state: FSMContext) -> None:
    if check_state_number(message.text):
        await state.update_data(change_state_number=message.text)
        await set_user_info_change_for_admin(message=message, state=state)
        return
    try:
        state_dict: dict = await state.get_data()
        await bot.edit_message_text(text="<b>Неправильно введён государственный номер.</b> \n"
                                         "Например: <b>А000АА|(регион)</b>",
                                    chat_id=state_dict['chat_id'],
                                    message_id=state_dict['behind_message'],
                                    reply_markup=change_user_info_preview_step)
        await message.delete()
    except MessageNotModified:
        pass
    except MessageToDeleteNotFound:
        pass


async def accept_changes_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    data: dict = await state.get_data()
    # print(data)
    states_list_for_admin: List[str] = [
        'change_initials_for_admin',
        'change_email_for_admin',
        'change_phone_for_admin',
        'change_group_for_admin',
        'change_car_mark_for_admin',
        'change_state_number_for_admin'
    ]
    for key in states_list_for_admin:
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
                                      reply_markup=select_accept_menu)
    except MessageNotModified:
        pass


async def agree_changes_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    _application = await state.get_data()
    print(_application)

    states_list: List[str] = [
        'change_initials',
        'change_email',
        'change_phone',
        'change_group',
        'change_car_mark',
        'change_state_number'
    ]
    for key in states_list:
        if _application[key] == 'без изменений':
            _application[key] = ''

    try:
        await state.update_data(data={
            'user_id': _application['user_id'],
            'change_initials': _application['change_initials'],
            'change_email': _application['change_email'],
            'change_phone': _application['change_phone'],
            'change_group': _application['change_group'],
            'change_car_mark': _application['change_car_mark'],
            'change_state_number': _application['change_state_number']
        })
        await confirm_approve_change_user_info_for_admin(query=query, state=state)
    except MessageNotModified:
        pass


async def confirm_approve_change_user_info_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    application_dict: dict = await state.get_data()
    application = await get_serialized_application(application_dict["data"]["__values__"], True)
    _successful: bool = await update_user(application)
    if _successful:
        try:
            await query.message.edit_text("Успешно обновлены данные!", reply_markup=back_inline_menu)
            # await drop_application(application)
        except MessageNotModified:
            pass


async def cancel_changes_for_admin(query: CallbackQuery, state: FSMContext) -> None:
    await preview_step(query=query, state=state)


async def continue_changes(query: CallbackQuery) -> None:
    try:
        await query.message.answer(f"Сохранено! \n"
                                   f"Выберите пункт (Несколько), который хотите изменить:\n",
                                   reply_markup=change_info_list_menu)
    except MessageNotModified:
        pass
