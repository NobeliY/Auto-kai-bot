from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_change_user_info_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("По ID", callback_data="get_user_by_id"),
            # InlineKeyboardButton("По ФИО", callback_data="get_user_by_initials"),
        ],
        # [
        #     InlineKeyboardButton("По номеру телефона", callback_data="get_user_by_phone"),
        # ],
        # [
        #   InlineKeyboardButton("По группе", callback_data="get_user_by_group"),
        #   InlineKeyboardButton("По Гос. Номеру", callback_data="get_user_by_state_number"),
        # ],
        [
            InlineKeyboardButton("Назад", callback_data="preview_step"),
        ],
    ]
)
select_searched_user_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Изменить", callback_data="selected_change_user_info")
        ], [
            InlineKeyboardButton("Назад", callback_data="preview_step")

        ],

    ]
)
# select_fully_show_user_info_searched_menu = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton("Подробнее", callback_data="show_fully_searched_user_info"),
#         ]
#     ]
# )

select_accept_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data="select_accept"),
            InlineKeyboardButton("Нет", callback_data="decline_accept"),
        ],
    ]
)

change_info_list_menu_admin: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить ФИО", callback_data="change_initials_admin"),
        ],
        [
            InlineKeyboardButton(text="Изменить почту", callback_data="change_email_admin"),
        ],
        [
            InlineKeyboardButton(text="Изменить номер телефона", callback_data="change_phone_admin"),
        ],
        [
            InlineKeyboardButton(text="Изменить группу", callback_data="change_group_admin"),
        ],
        [
            InlineKeyboardButton(text="Изменить модель автомобиля", callback_data="change_car_mark_admin"),
        ],
        [
            InlineKeyboardButton(text="Изменить Гос. номер", callback_data="change_state_number_admin"),
        ],
        [
            InlineKeyboardButton(text="Завершить изменение", callback_data="finish_changes_admin"),
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel_changes_admin")
        ]
    ]
)

change_user_info_preview_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="preview_step"),
        ],
    ]
)
