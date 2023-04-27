from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

change_info_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить данные", callback_data="change_info_menu"),
        ],
        [
            InlineKeyboardButton(text="Закрыть", callback_data="close_info"),
        ],
    ],
)

close_inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Закрыть", callback_data="close_info"),
        ]
    ]
)

change_info_list_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить ФИО", callback_data="change_initials"),
        ],
        [
            InlineKeyboardButton(text="Изменить почту", callback_data="change_email"),
        ],
        [
            InlineKeyboardButton(text="Изменить номер телефона", callback_data="change_phone"),
        ],
        [
            InlineKeyboardButton(text="Изменить группу", callback_data="change_group"),
        ],
        [
            InlineKeyboardButton(text="Изменить Гос. номер", callback_data="change_state_number"),
        ],
        [
            InlineKeyboardButton(text="Завершить изменение", callback_data="finish_changes"),
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel_changes")
        ]
    ]
)

accept_changes_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="agree_changes")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel_changes")
        ]
    ]
)
preview_step_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Назад", callback_data="preview_step")
        ]
    ]
)
