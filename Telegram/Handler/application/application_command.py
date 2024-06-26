import logging
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, MessageCantBeEdited

from Handler.default.start_command import start, get_admins_id_list
from Handler.help.help_fork import send_help_fork
from Keyboard.Inline.application_keyboard import select_application_mode_kb
from states import ApplicationSubmission, UserState
from utils.database_api.quick_commands import add_application, get_user
from utils.shared_methods.default import check_phone, check_email, check_initials, \
    send_user_application_info


async def select_application_mode(message: Message, state: FSMContext) -> None:
    user = await get_user(message.chat.id)
    if user:
        await message.answer(f"Вы зарегистрированы в боте!\n"
                             f"Используйте команду: <b>/start</b>")
        return
    await state.reset_state()
    await message.answer(f"<b>Выберите способ отправки заявления</b>",
                         reply_markup=select_application_mode_kb)
    await ApplicationSubmission.select_mode.set()
    return


async def set_application(query: CallbackQuery, state: FSMContext):
    await state.set_data({
        "user_id": query.from_user.id
    })
    await query.message.answer(f"<b>Вы начали подачу заявления</b> \n"
                               f"<b>Введите ФИО: </b>",
                               reply_markup=ReplyKeyboardRemove())
    await ApplicationSubmission.user_initials.set()


async def application_submission_initials(message: Message, state: FSMContext):
    if await check_message_text(message, state):
        if check_initials(message.text):
            await state.update_data(user_initials=message.text)
            await message.answer("<b>Введите E-mail: </b>")
            await ApplicationSubmission.user_email.set()
            return
        try:
            await message.edit_text("ФИО должно содержать только Буквы.")
        except MessageCantBeEdited:
            pass


async def application_submission_email(message: Message, state: FSMContext):
    if await check_message_text(message, state):
        if check_email(message.text):
            await state.update_data(user_email=message.text)
            await message.answer("<b>Введите номер телефона: </b>",
                                 )
            await ApplicationSubmission.user_phone_number.set()
            return
        await message.answer("<b>Неправильно введён E-mail.</b> \n"
                             "Например: <b>prime@example.com</b>")
        return


async def application_submission_phone(message: Message, state: FSMContext):
    if await check_message_text(message, state):

        if check_phone(message.text):
            await state.update_data(user_phone_number=message.text)
            await message.answer("<b>Введите Академическую группу: </b>",
                                 )
            await ApplicationSubmission.user_academy_group.set()
            return
        await message.answer("<b>Неправильно введён номер телефона.</b> \n"
                             "Например: <b>89999999999</b>")
        return


async def application_submission_academy_group(message: Message, state: FSMContext):
    if await check_message_text(message, state):
        await state.update_data(user_academy_group=message.text)
        await message.answer("<b>Введите модель автомобиля: </b>"
                             "Например: <b>Infinity QX</b>",
                             )
        await ApplicationSubmission.user_car_mark.set()


async def application_submission_car_mark(message: Message, state: FSMContext):
    if await check_message_text(message, state):
        await state.update_data(car_mark=message.text)
        await message.answer("<b>Введите Государственный номер: </b>"
                             "Например: <b>А000АА|(регион)</b>",
                             )
        await ApplicationSubmission.user_state_number.set()


async def application_submission_state_number(message: Message, state: FSMContext):
    if await check_message_text(message, state):
        state_regex_compiled = re.compile(r"\w\d{3}\w{2}\|\d")
        if re.search(state_regex_compiled, message.text.lower()):
            await state.update_data(user_state_number=message.text)
            user_application = await state.get_data()
            await add_application(
                user_id=user_application['user_id'],
                initials=user_application['user_initials'],
                email=user_application['user_email'],
                phone_number=user_application['user_phone_number'],
                group=user_application['user_academy_group'],
                car_mark=user_application['car_mark'],
                state_number=user_application['user_state_number'],

            )
            logging.info(f"Application: {','.join(user_application)}")
            await message.answer("<b>Данные были отправлены. Ожидайте письма с подтверждением на указанный вами "
                                 "почты.</b>",
                                 )
            await UserState.in_active.set()
            [
                await send_user_application_info(telegram_id=admin_id,
                                                 message=f"Добавлена новая заявка!")
                for admin_id in await get_admins_id_list()
            ]
        else:
            await message.answer("<b>Неправильно введён государственный номер.</b> \n"
                                 "Например: <b>А000АА|(регион)</b>")
            return


async def check_message_text(message: Message, state: FSMContext) -> bool:
    if message.text in ["/start", "/application", "/help"]:
        await state.finish()
        match message.text:
            case "/start":
                await start(message, state)
            case "/application":
                await select_application_mode(message, state)
            case "/help":
                await send_help_fork(message)
        return False
    return True


# Application from Web App
async def application_from_web_app(message: Message):
    logging.warning(message.web_app_data.data)
    # await bot.send_message(message.chat.id, message.web_app_data)
