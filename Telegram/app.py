import os

from aiogram import Bot, Dispatcher, executor

from loader import storage

# bot_token = "2087412404:AAFg-yxiGL9kURZDR5DLsDmhdI4cALeQqpM"
bot_token = os.getenv("BOT_TOKEN")
bot = Bot(bot_token)  # type: ignore

dp = Dispatcher(bot=bot, storage=storage)

# TODO: Main
if __name__ == "__main__":
    from handler import dp, get_default_commands
    executor.start_polling(dp, skip_updates=True, on_startup=get_default_commands)
