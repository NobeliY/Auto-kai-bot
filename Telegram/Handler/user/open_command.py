import logging as logger
from threading import Thread
from time import sleep

from aiogram.types import Message, ReplyKeyboardRemove
from colorama import Fore

from utils.database_api.quick_commands import add_parking_log, get_user
from utils.shared_methods.default import checkout, soon_info, return_user_checked, get_free_positions_on_parking
from utils.request_api.Request_controller import RequestController
from utils.request_api.request_to_ESP import send_level

activate_on_level = ['E', 'A']


def user_opened_task():
    sleep(20)


opened_loop = Thread(target=user_opened_task)



async def open_from_all_registered_users(message: Message):
    global opened_loop
    if opened_loop.is_alive():
        await message.answer(f"Уже открыт")
        return
    request_controller = RequestController(message.from_id)
    user_ = await get_user(user_id=message.from_id)
    access: str | None = await request_controller.check_user_on_database()
    if access is not None:
        template = await get_free_positions_on_parking()
        if access == "I":
            if template["left"] >= 1 and template["right"] >= 15:
                checker = await checkout()
                if not checker["out"]:
                    await message.answer(f"Нет свободных мест")
                    return
        if access == "S":
            if template["right"] >= 15:
                checker = await checkout()
                if not checker["out"]:
                    await message.answer(f"Нет свободных мест")
                    return
        if await request_controller.check_time(access):
            await request_controller.check_date_quality()
            request_data = await send_level(message.from_id)
            try:
                if request_data['value']:
                    await message.answer("Добро пожаловать! Шлагбаум автоматически закроется через 20 секунд.")
                    opened_loop = Thread(target=user_opened_task)
                    opened_loop.start()
                    await add_parking_log(user_id=user_.id, initials=user_.initials)
            except KeyError:
                logger.error(f"{Fore.LIGHTRED_EX}KeyError with request :"
                             f"{Fore.LIGHTWHITE_EX}1{Fore.LIGHTRED_EX} level. (S|I|T){Fore.RESET}")

        else:
            await message.answer(f" Диапазон от 6 до 23")
    else:
        await message.answer(return_user_checked(False),
                             reply_markup=ReplyKeyboardRemove())
    await message.delete()


async def open_first_level_from_employee(message: Message):
    logger.warning("Catch Open First")
    request_controller = RequestController(message.from_id)
    access = await request_controller.check_user_on_database()
    if access is None or access not in activate_on_level:
        return
    await request_controller.check_date_quality()

    request_data = await send_level(message.from_id)
    try:
        if request_data['value']:
            user_ = await get_user(message.from_id)
            await add_parking_log(user_id=user_.id, initials=user_.initials)
            await message.answer("Добро пожаловать! Шлагбаум автоматически закроется через 20 секунд.")
    except KeyError:
        logger.error(f"{Fore.LIGHTRED_EX}KeyError with request :"
                     f"{Fore.LIGHTWHITE_EX}1{Fore.LIGHTRED_EX} level. (E|A){Fore.RESET}")

    await message.delete()


async def open_second_level_from_employee(message: Message):
    request_controller = RequestController(message.from_id)
    access = await request_controller.check_user_on_database()
    if access is None or access not in activate_on_level:
        return
    # user_ = await get_user(message.from_id)
    # await add_parking_log(user_id=user_.id, initials=user_.initials)
    await message.answer(await soon_info())
    await message.delete()
