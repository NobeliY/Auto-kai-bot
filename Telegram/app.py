import os
import logging
from aiogram import Bot, Dispatcher, executor


from states.loader import storage

# logging.basicConfig(level=logging.INFO)
bot_token = os.getenv("BOT_TOKEN")
bot = Bot(bot_token)  # type: ignore

dp = Dispatcher(bot=bot, storage=storage)

# TODO: Main
if __name__ == "__main__":
    from Handler import dp
    from Handler.default import get_default_commands
    executor.start_polling(dp, skip_updates=True, on_startup=get_default_commands)
