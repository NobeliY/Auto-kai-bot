from threading import Thread
from time import sleep

from Handler import soon_info
from Keyboard.InlineKeyboard import main_admin_menu
# TODO: Import a Custom Modules
from app import dp
from Handler.bot_default import return_user_checked, get_access_level, get_reply_keyboard
from states import UserState

# TODO: Import Aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

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
    # await state.finish()


# TODO: Reply Text
@dp.message_handler(state=UserState.in_active)
async def keyboard_on_registered_users(message: types.Message, state: FSMContext):
    activate_on_level = ['E', 'A']
    request_controller = RequestController(message.from_id)
    global opened_loop
    match message.text:
        case "Выйти":
            await state.finish()
        case "Открыть":
            if opened_loop.is_alive():
                await message.answer(F"Уже открыт")
            else:
                access = await request_controller.check_user_on_database()
                if access is not None:
                    if await request_controller.check_time(access):
                        await request_controller.check_date_quality()
                        await message.answer(return_user_checked(True))

                        opened_loop = Thread(target=user_opened_task)
                        opened_loop.start()
                    else:
                        await message.answer(f" Диапазон от 6 до 23")
                else:
                    await message.answer(return_user_checked(False),
                                         parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())

        case "Открыть 1 уровень":
            access = await request_controller.check_user_on_database()
            if access is not None and access in activate_on_level:
                await message.answer(f"{return_user_checked(True)} 1")
            else:
                await message.answer(return_user_checked(False),
                                     parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())

        case "Открыть 2 уровень":
            await message.answer(await soon_info())
            # access = await request_controller.check_user_on_database()
            # if access is not None and access in activate_on_level:
            #     await message.answer(f"{return_user_checked(user_registered=True)} 2")
            # else:
            #     await message.answer(return_user_checked(False))

        case "Информация о себе":
            user = await get_user(message.from_id)
            await message.answer(
                f"Информация о Вас! \n"
                f"Ваш Telegram ID: <b>{user.id}</b>\n"
                f"ФИО: <b>{user.initials}</b>\n"
                f"Почта: <b>{user.email}</b>\n"
                f"Номер телефона: <b>{user.phoneNumber}</b>\n"
                f"Гос. номер используемого транспорта: <b>{user.stateNumber}</b>\n"
                f"Уровень: <b>{get_access_level(user.access)}</b>\n",
                parse_mode=types.ParseMode.HTML
            )

        case "Свободные места":
            await message.answer(await soon_info())

        case "Панель для администратора.":
            if not await get_admin_level(request_controller=request_controller):
                return
            user = await get_user(message.from_id)
            await message.answer(f"Добро пожаловать, <b>{user.initials}</b>!",
                                 parse_mode=types.ParseMode.HTML, reply_markup=main_admin_menu)


async def get_admin_level(request_controller: RequestController):
    return await request_controller.check_user_on_database() == 'A'
