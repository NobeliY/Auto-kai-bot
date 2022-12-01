import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from states.loader import storage
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
bot = Bot(bot_token)  # type: ignore

dp = Dispatcher(bot=bot, storage=storage)

# TODO: Main
if __name__ == "__main__":
    from Handler import dp
    from Handler.default import get_default_commands

    executor.start_polling(dp, skip_updates=True, on_startup=get_default_commands)
