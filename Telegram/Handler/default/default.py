import logging as logger
import os
from typing import List
import subprocess
from multiprocessing import Process

from app import bot
from aiogram import types, Dispatcher
import aiogram.utils.exceptions as exceptions
from colorama import Fore
# import schedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from Data import admins
from Handler.handler import register_handlers
from utils.database_api.database_gino import on_startup, on_close
from utils.database_api.quick_commands import get_users_info, get_admins_id
from utils.request_api.request_to_ESP import send_reboot_command_from_esp
# from utils.shared_methods.default import set_on_startup_users

def reboot_esp():
    send_reboot_command_from_esp()

def run_computer_vision():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    path = os.path.join(desktop, "Auto-kai-bot", "ComputerEyes")
    with open(os.path.join(path, "cv_log.log"), "w", encoding="utf-8") as f:
        computer_vision_process = subprocess.Popen([
            os.path.join(path, "run.bat")
        ],
        shell=True,
        stdout=f)
        

def run_process_cv():
    process_cv = Process(target=run_computer_vision)
    process_cv.start()
    process_cv.join()


async def get_default_commands(dp: Dispatcher) -> None:
    try:
        on_close()
    except Exception as _ex:
        logger.error(f"{Fore.LIGHTRED_EX}{_ex} | On Close Exception {Fore.RESET}")
    await on_startup()
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Начало Работы / Обновить бота."),
            types.BotCommand("application", "Заявление."),
            types.BotCommand("help", "Инструкция по эксплуатации. 🧐")
        ]
    )
    # set_on_startup_users([
    #     user.id for user in await get_users_info()
    # ])
    logger.info(f"{Fore.GREEN}Бот запущен{Fore.RESET}!")

    try:
        await bot.send_message(chat_id=834865678, text=" Бот возобновил работу.")
    except exceptions.ChatNotFound:
        logger.warning(f"{Fore.RED}Нет чата с 834865678{Fore.RESET}!")
    register_handlers(dp=dp)
    logger.info(f"{Fore.LIGHTGREEN_EX}Register handlers job done{Fore.RESET}!")

    # schedule.every(5).hours.do(reboot_esp)
    reboot_scheduler = AsyncIOScheduler()
    reboot_scheduler.add_job(reboot_esp, 'interval', hours=1)
    # run_process_cv()
    # schedule.every(1).hour.do(run_process_cv)
    cv_scheduler = AsyncIOScheduler()
    cv_scheduler.add_job(run_process_cv, 'interval', minutes=10)
    cv_scheduler.start()
    reboot_scheduler.start()
