import logging
import os

from colorama import Fore
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor

from states.loader import storage

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
bot = Bot(bot_token)
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.WARNING, format=f"{Fore.YELLOW}%(asctime)s {Fore.RESET}| [{Fore.CYAN}%(levelname)s"
                                                  f"{Fore.RESET}] %(message)s")

# TODO: Main
if __name__ == "__main__":
    from Handler.default.default import get_default_commands

    executor.start_polling(dp, skip_updates=True, on_startup=get_default_commands)
