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


async def send_level(user_id: int, first_level: bool = True) -> dict | str:
    request_ = send_request_from_esp(set_post_json_dict(user_id=user_id,
                                                        level=first_secret_key if first_level else second_secret_key))
    request_['error'] = request_['error'].replace('<', '{').replace('>', '}')
    if 'error' in request_.keys():
        await bot.send_message(admins[0], f"User: {user_id} | Error: {request_['error']}")
        logger.error(f"{Fore.LIGHTRED_EX}User: {user_id} | {request_['error']}{Fore.RESET}")
        return {
            'value': 0,
        }
    return request_


def send_request_from_esp(post_json_data: dict) -> dict | str:
    try:
        with Session() as session:
            with session.post(url=request_uri, data=post_json_data) as response:
                return response.json()
    except ConnectionError as connection_error:
        # logger.error(f"{type(connection_error)} \n {connection_error.__str__()}")
        return {
            'error': connection_error.__str__()
        }
        # return f"{Fore.LIGHTRED_EX}User: {post_json_data['user_id']} | {connection_error.strerror}{Fore.RESET}"
    except Timeout as server_error:
        return {
            'error': server_error.__str__()
        }
        # return f"{Fore.LIGHTRED_EX}User: {post_json_data['user_id']} | {server_error.strerror}{Fore.RESET}"
