from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from Data.config import WEB_APP_URL

select_application_mode_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            # InlineKeyboardButton(text="Новый вариант подачи.",
            #                web_app=WebAppInfo(url=WEB_APP_URL)),
            InlineKeyboardButton(text="Старый вариант подачи."),

        ],
    ],
    # resize_keyboard=True
)
