from time import sleep
from threading import Thread

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ParseMode, ReplyKeyboardRemove

from Handler.default import return_user_checked, soon_info
from app import dp
from states import UserState
from utils.request_api.Request_controller import RequestController

activate_on_level = ['E', 'A']


def user_opened_task():
    sleep(20)


opened_loop = Thread(target=user_opened_task)


@dp.message_handler(Text(equals="открыть", ignore_case=True),
                    state=UserState.all_states)
async def open_from_all_registered_users(message: Message, state: FSMContext):
    global opened_loop
    if opened_loop.is_alive():
        await message.answer(f"Уже открыт")
        return
    request_controller = RequestController(message.from_id)
    print(request_controller)
    access = await request_controller.check_user_on_database()
    if access is not None:
        if await request_controller.check_time(access):
            await request_controller.check_date_quality()
            await message.answer(return_user_checked())

            opened_loop = Thread(target=user_opened_task)
            opened_loop.start()
        else:
            await message.answer(f" Диапазон от 6 до 23")
    else:
        await message.answer(return_user_checked(False),
                             parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Открыть 1 уровень", ignore_case=True),
                    state=UserState.all_states)
async def open_first_level_from_employee(message: Message, state: FSMContext):
    request_controller = RequestController(message.from_id)
    print(request_controller)
    access = await request_controller.check_user_on_database()
    if access is None or access not in activate_on_level:
        return
    await request_controller.check_date_quality()

    await message.answer(return_user_checked())


@dp.message_handler(Text(equals="Открыть 2 уровень", ignore_case=True),
                    state=UserState.all_states)
async def open_second_level_from_employee(message: Message, state: FSMContext):
    request_controller = RequestController(message.from_id)
    access = await request_controller.check_user_on_database()
    if access is None or access not in activate_on_level:
        return
    await message.answer(await soon_info())
