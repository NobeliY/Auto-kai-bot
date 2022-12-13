import re

from Handler import start
from states import ApplicationSubmission

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.database_api.quick_commands import add_application


async def set_application(message: types.Message, state: FSMContext):
    await state.reset_state()
    await state.update_data(user_id=message.from_id)
    await message.answer(f"<b>Вы начали подачу заявления</b> \n"
                         f"<b>Введите ФИО: </b>",
                         parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    await ApplicationSubmission.user_initials.set()


async def application_submission_initials(message: types.Message, state: FSMContext):
    if message.text == "/start":
        await state.finish()
        await start(message, state)
    else:
        await state.update_data(user_initials=message.text)
        await message.answer("<b>Введите E-mail: </b>",
                             parse_mode=types.ParseMode.HTML)
        await ApplicationSubmission.user_email.set()


async def application_submission_email(message: types.Message, state: FSMContext):
    email_address_re_compile = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if re.search(email_address_re_compile, message.text):
        await state.update_data(user_email=message.text)
        await message.answer("<b>Введите номер телефона: </b>",
                             parse_mode=types.ParseMode.HTML)
        await ApplicationSubmission.user_phone_number.set()
    else:
        await message.answer("<b>Неправильно введён E-mail.</b> \n"
                             "Например: <b>prime@example.com</b>", parse_mode=types.ParseMode.HTML)
        return


async def application_submission_phone(message: types.Message, state: FSMContext):
    phone_number_re_compile = re.compile(r"\d{11}")
    if re.fullmatch(phone_number_re_compile, message.text):
        await state.update_data(user_phone_number=message.text)
        await message.answer("<b>Введите Академическую группу: </b>",
                             parse_mode=types.ParseMode.HTML)
        await ApplicationSubmission.user_academy_group.set()
    else:
        await message.answer("<b>Неправильно введён номер телефона.</b> \n"
                             "Например: <b>89999999999</b>", parse_mode=types.ParseMode.HTML)
        return


async def application_submission_academy_group(message: types.Message, state: FSMContext):
    await state.update_data(user_academy_group=message.text)
    await message.answer("<b>Введите Государственный номер: </b>"
                         "Например: <b>А000АА|(регион)</b>",
                         parse_mode=types.ParseMode.HTML)
    await ApplicationSubmission.user_state_number.set()


async def application_submission_state_number(message: types.Message, state: FSMContext):
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
            state_number=user_application['user_state_number'],

        )
        await message.answer("<b>Данные были отправлены. Ожидайте письма с подтверждением на указанный вами почты.</b>",
                             parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("<b>Неправильно введён государственный номер.</b> \n"
                             "Например: <b>А000АА|(регион)</b>", parse_mode=types.ParseMode.HTML)
        return
