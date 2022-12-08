from threading import Thread
from time import sleep

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ParseMode, ReplyKeyboardRemove

from Handler.default import return_user_checked, soon_info
from app import dp
from Data import __all_states__
from states import UserState, Admins
from utils.request_api.Request_controller import RequestController
from utils.request_api.request_to_ESP import send_first_level

activate_on_level = ['E', 'A']


def user_opened_task():
    sleep(20)


opened_loop = Thread(target=user_opened_task)


@dp.message_handler(Text(equals="открыть", ignore_case=True),
                    state=UserState.all_states)
async def open_from_all_registered_users(message: Message):
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
            request_data = await send_first_level(message.from_id)
            try:
                if request_data['value']:
                    await message.answer("Добро пожаловать! Шлагбаум автоматически закроется через 20 секунд.")
            except KeyError:
                print("KeyError with request 1 level. (S|I|T)")

            opened_loop = Thread(target=user_opened_task)
            opened_loop.start()
        else:
            await message.answer(f" Диапазон от 6 до 23")
    else:
        await message.answer(return_user_checked(False),
                             parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    await message.delete()


@dp.message_handler(Text(equals="Открыть 1 уровень", ignore_case=True),
                    state=__all_states__)
async def open_first_level_from_employee(message: Message):
    request_controller = RequestController(message.from_id)
    access = await request_controller.check_user_on_database()
    if access is None or access not in activate_on_level:
        return
    await request_controller.check_date_quality()

    request_data = await send_first_level(message.from_id)
    try:
        if request_data['value']:
            await message.answer("Добро пожаловать! Шлагбаум автоматически закроется через 20 секунд.")
    except KeyError:
        print("KeyError with request 1 level. (E|A)")

    await message.delete()


@dp.message_handler(Text(equals="Открыть 2 уровень", ignore_case=True),
                    state=UserState.all_states)
@dp.message_handler(Text(equals="Открыть 2 уровень", ignore_case=True),
                    state=Admins.all_states)
async def open_second_level_from_employee(message: Message):
    request_controller = RequestController(message.from_id)
    access = await request_controller.check_user_on_database()
    if access is None or access not in activate_on_level:
        return
    await message.answer(await soon_info())
    await message.delete()
