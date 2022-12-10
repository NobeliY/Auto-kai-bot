from aiogram.types import Message, ParseMode


async def send_help_fork(message: Message):
    await message.answer("👋 Вас приветствует бот для <b>АФ \"КНИТУ-КАИ\"</b>,"
                         "предназначенный для автоматизации въезда и выезда с автомобильной парковки.\n"
                         "Список команд:\n"
                         "<b>/start</b> - Запуск или перезапуск меня.\n"
                         "<b>/application</b> - Отправки заявку на получение доступа на парковку.\n"
                         "<b>/help</b> - Вызов помощи по боту.\n"
                         "Спасибо за использование данного бота 😃",
                         parse_mode=ParseMode.HTML)
    await message.delete()
