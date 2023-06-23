import logging as logger
from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from colorama import Fore

from utils.shared_methods.default import get_access_level, user_to_str
from Keyboard.Inline import back_inline_menu
from Keyboard.Inline import delete_accept_menu, delete_fully_show_searched_menu, \
    delete_searched_user_button
from states import Admins
from utils.database_api.quick_commands import delete_users_by_group, get_users_by_group, get_users_by_initials, \
    delete_user_by_initials_command, get_serialized_user
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
