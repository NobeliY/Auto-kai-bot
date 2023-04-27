import logging as logger
from os import getenv

from requests import Session, ConnectionError, Timeout
from colorama import Fore

from Data import admins
from app import bot
from utils.database_api.schemas import User

request_uri, first_secret_key, second_secret_key = getenv("REQUEST_ESP").split()


def set_post_json_dict(user_id: User.id, level: str) -> dict:
    return {
        "secret_key": level,
        "user_id": user_id
    }


async def send_first_level(user_id: int) -> dict:
    return send_request_from_esp(set_post_json_dict(user_id=user_id, level=first_secret_key))


async def send_second_level(user_id: int) -> dict:
    return send_request_from_esp(set_post_json_dict(user_id=user_id, level=second_secret_key))


def send_request_from_esp(post_json_data: dict) -> dict:
    try:
        with Session() as session:
            with session.post(url=request_uri, data=post_json_data) as response:
                return response.json()
    except ConnectionError as connection_error:
        error_msg: str = f"{Fore.LIGHTRED_EX}User: {post_json_data['user_id']} | {connection_error}{Fore.RESET}"
        await bot.send_message(admins[0], error_msg)
        logger.error(error_msg)
        return {
            'value': 0,
        }
    except Timeout as server_error:
        error_msg: str = f"{Fore.LIGHTRED_EX}User: {post_json_data['user_id']} | {server_error}{Fore.RESET}"
        await bot.send_message(admins[0], error_msg)
        logger.error(error_msg)
        return {
            'value': 0,
        }
