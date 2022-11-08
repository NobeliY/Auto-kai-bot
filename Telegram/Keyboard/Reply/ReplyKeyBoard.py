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
            KeyboardButton(text="Открыть 2 уровень"),
        ],
        [
            KeyboardButton(text="Открыть 1 уровень"),

        ]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    [
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
            KeyboardButton(text="Открыть 2 уровень"),
        ],
        [
            KeyboardButton(text="Открыть 1 уровень"),
        ]
    ],
    resize_keyboard=True
)
