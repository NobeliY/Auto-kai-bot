from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

select_application_mode_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            # InlineKeyboardButton(text="Новый вариант подачи.",
            #                web_app=WebAppInfo(url=WEB_APP_URL)),
            InlineKeyboardButton(text="Старый вариант подачи.", callback_data="old_type"),

        ],
    ],
    # resize_keyboard=True
)
