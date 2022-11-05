from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Посмотреть БД", callback_data="users_info"),
        ],
        [
            InlineKeyboardButton("Добавить пользователя", callback_data="user_add_menu"),
            InlineKeyboardButton("Удалить", callback_data="user_remove_menu"),
        ],
        [
            InlineKeyboardButton("Просмотреть заявки", callback_data="show_applications"),
        ],
    ],
)

add_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("", callback_data="auto_add_by_application"),
        ],
        [
            InlineKeyboardButton("", callback_data="manual_add"),
        ],
    ]
)
