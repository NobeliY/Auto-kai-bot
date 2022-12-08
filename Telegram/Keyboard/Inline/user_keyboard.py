from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

change_info_menu = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить данные", callback_data="change_info_menu"),
        ],
    ],
)
