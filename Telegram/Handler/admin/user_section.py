from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ParseMode, ContentTypes

from Handler.default import get_access_level
from Keyboard.Inline import back_inline_menu
from Keyboard.Inline import delete_accept_menu, delete_fully_show_searched_menu,\
    delete_searched_user_button
from app import dp, bot
from states import Admins
from utils.database_api.quick_commands import delete_users_by_group, get_users_by_group, get_users_by_initials,\
    delete_user_by_initials_command
from utils.database_api.schemas.user import User


@dp.callback_query_handler(Text(equals="delete_by_initials"),
                           state=Admins.delete_menu_state)
async def delete_user_by_initials(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.searched_user_delete_state)
    await query.message.answer("Введите ФИО (Можно Фамилию имя). \n"
                               "Рекомендуется вводить ФИО полностью")


@dp.message_handler(content_types=ContentTypes.TEXT,
                    state=Admins.searched_user_delete_state)
async def delete_user_by_initials_searched(message: Message, state: FSMContext):
    users = await get_users_by_initials(initials=message.text)
    if not users:
        await message.answer("Нет пользователя с такими ФИО.", reply_markup=back_inline_menu)
        return
    if len(users) == 1:
        user = users[-1]
        await message.answer(f"Вы точно хотите удалить {user.initials}?",
                             reply_markup=delete_accept_menu)
        await state.update_data(data={
            "data": user,
        })
        return
    await message.answer(f"По вашему запросу найдено: <b>{len(users)}</b>\n"
                         f"Нажмите на `Подробнее` и выберите из сообщений необходимый!",
                         parse_mode=ParseMode.HTML,
                         reply_markup=delete_fully_show_searched_menu)
    await state.update_data(data={
        "data": users
    })


@dp.callback_query_handler(Text(equals="show_fully_searched_users"),
                           state=Admins.searched_user_delete_state)
async def send_all_searched_users_for_delete(query: CallbackQuery, state: FSMContext):
    users = await state.get_data()
    [
        await query.message.answer(f"Telegram ID: <b>{user.id}</b>\n"
                                   f"ФИО: <b>`{user.initials}`</b>\n"
                                   f"Почта: <b>{user.email}</b>\n"
                                   f"Группа: <b>{user.group}</b>\n"
                                   f"Номер телефона: <b>{user.phoneNumber}</b>\n"
                                   f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
                                   f"Уровень: <b>{get_access_level(user.access)}</b>\n",
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=delete_searched_user_button)
        for user in users['data']
    ]


@dp.callback_query_handler(Text(equals="selected_user_for_delete"),
                           state=Admins.searched_user_delete_state)
async def delete_user_question(query: CallbackQuery, state: FSMContext):
    initials = query.message.text.split("`")[1]
    try:
        await query.message.delete()
    except Exception as ex_:
        print(f"Error: {ex_}")
        await query.message.edit_text("Ничего нет!")
    await query.message.answer(f"Вы точно хотите удалить {initials}",
                               reply_markup=delete_accept_menu)
    users = await get_users_by_initials(initials=initials)
    await state.update_data(data={
        "data": users[0]
    })


@dp.callback_query_handler(Text(equals="accept_delete"),
                           state=Admins.searched_user_delete_state)
async def delete_user(query: CallbackQuery, state: FSMContext):
    users = await state.get_data()
    user = users['data']
    await delete_user_by_initials_command(user=user)
    await query.message.edit_text(f"Успешно удален:\n"
                                  f"Telegram ID: <b>{user.id}</b>\n"
                                  f"ФИО: <b>{user.initials}</b>\n"
                                  f"Почта: <b>{user.email}</b>\n"
                                  f"Группа: <b>{user.group}</b>\n"
                                  f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
                                  f"Уровень: <b>{get_access_level(user.access)}</b>\n",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=back_inline_menu)


@dp.callback_query_handler(Text(equals="decline_delete"),
                           state=Admins.searched_user_delete_state)
async def decline_delete_user(query: CallbackQuery):
    await decline_delete(query)


@dp.callback_query_handler(Text(equals="delete_all_group"),
                           state=Admins.delete_menu_state)
async def delete_all_from_group(query: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.delete_all_group_state)
    await query.message.answer("Введите группу для удаления!")


@dp.message_handler(content_types=ContentTypes.TEXT,
                    state=Admins.delete_all_group_state)
async def get_group_for_delete(message: Message, state: FSMContext):
    users: List[User] | None = await get_users_by_group(group=message.text)
    if not users:
        await message.answer("Нет такой группы в БД.", reply_markup=back_inline_menu)
        return
    await message.answer(f"Найдено: <b>{len(users)}</b>\n"
                         f"Вы точно хотите удалить эту группу?",
                         reply_markup=delete_accept_menu,
                         parse_mode=ParseMode.HTML)
    await state.update_data(data={
        "data": users
    })


@dp.callback_query_handler(Text(equals="accept_delete"),
                           state=Admins.delete_all_group_state)
async def accept_delete_group(query: CallbackQuery, state: FSMContext):
    users = await state.get_data()
    await delete_users_by_group(users=users['data'])
    await query.message.edit_text(f"Успешна удалена группа: {query.message.text}",
                                  reply_markup=back_inline_menu)


@dp.callback_query_handler(Text(equals="decline_delete"),
                           state=Admins.delete_all_group_state)
async def decline_delete_group(query: CallbackQuery):
    await decline_delete(query)


async def decline_delete(query: CallbackQuery):
    await query.message.edit_text("<b>Операция отменена!</b>",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=back_inline_menu)
