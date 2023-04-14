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
            InlineKeyboardButton("Из заявок", callback_data="auto_add_by_application"),
            InlineKeyboardButton("Вручную", callback_data="manual_add"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)

add_by_applications_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Просмотр со старых", callback_data="start_from_begin"),
            InlineKeyboardButton("Просмотр с новых", callback_data="start_from_end"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)

manual_add_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Добавить", callback_data="start_manual_add"),
            InlineKeyboardButton("Отмена", callback_data="preview_step"),
        ]
    ]
)

cancel_manual_add_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Отменить добавление", callback_data="cancel_manual_add"),
        ]
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

delete_accept_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data="accept_delete"),
            InlineKeyboardButton("Нет", callback_data="decline_delete"),
        ],
    ]
)

delete_fully_show_searched_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Подробнее", callback_data="show_fully_searched_users"),
        ]
    ]
)

delete_searched_user_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Выбрать", callback_data="selected_user_for_delete"),
        ]
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

back_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)

application_change_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Следующая", callback_data="next_application"),
        ],
        [
          InlineKeyboardButton("Принять", callback_data="approve_application"),
          InlineKeyboardButton("Отклонить", callback_data="submit_reject_application"),
        ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ]
    ]
)

application_or_manual_submit_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Студент", callback_data="student"),
            InlineKeyboardButton("Студент+", callback_data="student_plus"),
        ],
        [
            InlineKeyboardButton("Преподаватель", callback_data="teacher"),
            InlineKeyboardButton("Сотрудник", callback_data="employee"),
        ],
        [
            InlineKeyboardButton("Администратор", callback_data="administrator"),
        ],
        [
            InlineKeyboardButton("Отмена", callback_data="preview_step")
        ],
    ]
)

manual_approve_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data="approve_manual"),
            InlineKeyboardButton("Нет", callback_data="cancel_manual_add")
        ],
    ]
)

application_approve_level_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data="approve_level_application"),
            InlineKeyboardButton("Нет", callback_data="preview_step")
        ],
    ]
)

application_reject_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data="reject_application"),
            InlineKeyboardButton("Нет", callback_data="preview_step")
        ],
    ]
)

application_close_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        InlineKeyboardButton("Закрыть", callback_data="close_application")
    ]
)
