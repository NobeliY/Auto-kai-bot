from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

student_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Информация о себе"),
        ],
        [
            KeyboardButton(text="Свободные места"),
        ],
        [
            KeyboardButton(text="Открыть"),
        ]
    ], resize_keyboard=True
)

teacher_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Информация о себе")
        ],
        [
            KeyboardButton(text="Свободные места"),
        ],
        [
            KeyboardButton(text="Открыть"),
        ]
    ],
    resize_keyboard=True
)

employee_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Свободные места"),
        ],
        [
            KeyboardButton(text="Информация о себе"),
        ],
        [
            KeyboardButton(text="Открыть железные ворота"),
        ],
        [
            KeyboardButton(text="Открыть шлагбаум"),
        ]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Отправить сообщение"),
        ],
        [
            KeyboardButton(text="Свободные места"),
        ],
        [
            KeyboardButton(text="Информация о себе"),
        ],
        [
            KeyboardButton(text="Панель для администратора")
        ],
        [
            KeyboardButton(text="Открыть железные ворота"),
        ],
        [
            KeyboardButton(text="Открыть шлагбаум"),
        ]
    ],
    resize_keyboard=True
)
