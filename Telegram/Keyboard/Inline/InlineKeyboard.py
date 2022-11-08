from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states import Admin

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
            InlineKeyboardButton("Из заявок", callback_data="auto_add_by_application"),
            InlineKeyboardButton("Вручную", callback_data="manual_add"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)

delete_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Удалить по ФИО", callback_data="delete_by_initials"),
            InlineKeyboardButton("Удалить всю группу", callback_data="delete_all_group"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)

show_applications_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("По очереди", callback_data="show_application"),
            InlineKeyboardButton("Все", callback_data="show_all_applications"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)

show_db_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Подробнее", callback_data="show_fully_information_from_db"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)
