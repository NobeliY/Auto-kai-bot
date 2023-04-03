from aiogram import types
from aiogram.dispatcher import FSMContext

import utils.shared_methods.default
from states import UserState
from utils.database_api.quick_commands import get_user


async def start(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await get_user(message.from_id)

    if user is None:
        await message.answer(utils.shared_methods.default.return_user_checked(False), parse_mode=types.ParseMode.HTML,
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(f"Добро пожаловать! \n"
                             f"|{utils.shared_methods.default.get_access_level(user.access)}| {user.initials}!\n"
                             f"Вызвана клавиатура с командами снизу!",
                             reply_markup=utils.shared_methods.default.get_reply_keyboard(user.access))
        await UserState.in_active.set()
    await message.delete()
