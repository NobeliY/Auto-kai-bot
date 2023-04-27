import logging

from colorama import Fore
from aiogram import Bot, Dispatcher, executor
from Data import BOT_TOKEN
from Data.config import LOGGING_LEVEL
from states.loader import storage

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=storage)
logging_level = LOGGING_LEVEL
logging.basicConfig(level=logging_level, format=f"{Fore.YELLOW}%(asctime)s {Fore.RESET}| [{Fore.CYAN}%(levelname)s"
                                                f"{Fore.RESET}] %(message)s")

# TODO: Main
if __name__ == "__main__":
    from Handler.default.default import get_default_commands

    executor.start_polling(dp, skip_updates=True, on_startup=get_default_commands)
