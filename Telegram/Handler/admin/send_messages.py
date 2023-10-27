import logging
from enum import Enum
from typing import Union, List
import time

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound, ChatNotFound, UserDeactivated

from Keyboard.Inline.admin_keyboard import send_message_menu_kb, reject_send_message_kb, message_approve_menu_kb
from app import bot
from states import Admins, UserState
from utils.database_api.quick_commands import get_user, get_users_by_access, get_all_users
from utils.database_api.schemas import User


async def get_send_message_menu(message: Message, state: FSMContext) -> None:
    user = await get_user(user_id=message.from_user.id)
    try:
        if user.access == "A":
            await Admins.send_message_state.set()
            await state.set_data(data={
                "message_id": message.message_id
            })
            await message.delete()
            await message.answer(text="Выберите, какой группе отправить сообщение:",
                                 reply_markup=send_message_menu_kb)
    except AttributeError:
        logging.error(f"Undefined user by id: {message.from_user.id}")
    except MessageToDeleteNotFound:
        pass


async def get_group_set_to_send(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_data(data={
        "group": query.data
    })
    await query.message.edit_text(f"Введите сообщение для отправки. (Можно использовать HTML tags)",
                                  reply_markup=reject_send_message_kb)


async def send_message_choice(message: Message, state: FSMContext) -> None:
    data: dict = await state.get_data()
    data["message"] = message.text
    await state.update_data(data=data)
    await message.answer(f"Вы уверены, что хотите отправить сообщение <b>{Send.__getitem__(data['group']).value}</b>:\n"
                         f"{message.text} ?", reply_markup=message_approve_menu_kb)


async def approve_send_message(query: CallbackQuery, state: FSMContext) -> None:
    data: dict = await state.get_data()
    await query.message.edit_text("Отправляю уведомление!")
    group: str = data["group"]
    match group:
        case "send_students":
            user_list: Union[List[User], None] = await get_users_by_access(access="S")
            user_list += await get_users_by_access(access="I")
            await send_message_from_users(user_list, data["message"])
            return
        case "send_employees":
            user_list: Union[List[User], None] = await get_users_by_access(access="T")
            user_list += await get_users_by_access(access="E")
            await send_message_from_users(user_list, data["message"], level="сотрудникам")
            return
        case "send_admins":
            user_list: Union[List[User], None] = await get_users_by_access(access="A")
            await send_message_from_users(user_list, data["message"], level="администраторам")
            return
        case "send_all":
            user_list: Union[List[User], None] = await get_all_users()
            await send_message_from_users(user_list, data["message"])
            return


async def send_message_from_users(user_list: Union[List[User], None], message: str,
                                  level: Union[str, None] = None) -> None:
    level_sends: Union[str, None] = None
    if level:
        level_sends = f"Данное сообщение отправлено <b>{level}</b>"
    if user_list:
        counter = 0
        for user in user_list:
            counter += 1
            try:
                logging.info(f"send message to: {user.id}")
                await bot.send_message(chat_id=user.id,
                                       text=f"Здравствуйте, <b>{user.initials}</b>! \n"
                                            f"Для вас уведомление от администратора!\n"
                                            f"{message}\n"
                                            f"{level_sends if level_sends else ''}",
                                       reply_markup=reject_send_message_kb)
            except Exception:
                logging.error(f"Chat not found: {user.id}")
            if counter == 5:
                time.sleep(1.0)
                counter = 0


async def close_send_message_menu(query: CallbackQuery, state: FSMContext) -> None:
    try:
        await state.reset_data()
        await UserState.in_active.set()
        await query.message.delete()
    except MessageToDeleteNotFound:
        await query.message.edit_text("Nothing")
        await query.message.delete()


class Send(Enum):
    send_students = "Студентам"
    send_employees = "Сотрудникам"
    send_admins = "Администраторам"
    send_all = "Всем"
