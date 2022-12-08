from threading import Thread
from time import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from Handler.default import return_user_checked, get_access_level, get_reply_keyboard
from app import dp
from states import UserState
from utils.database_api.quick_commands import get_user
from utils.request_api.Request_controller import RequestController


def user_opened_task():
    sleep(20)


opened_loop = Thread(target=user_opened_task)


@dp.message_handler(Command("start"), state="*")
async def start(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await get_user(message.from_id)

    if user is None:
        await message.answer(return_user_checked(False), parse_mode=types.ParseMode.HTML,
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(f"Добро пожаловать! \n"
                             f"|{get_access_level(user.access)}| {user.initials}!\n"
                             f"Вызвана клавиатура с командами снизу!",
                             parse_mode=types.ParseMode.HTML, reply_markup=get_reply_keyboard(user.access))
        await UserState.in_active.set()
    await message.delete()


async def get_admin_level(request_controller: RequestController):
    return await request_controller.check_user_on_database() == 'A'
