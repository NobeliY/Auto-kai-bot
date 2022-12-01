
from os import getenv
from aiohttp import ClientSession, ClientConnectionError, ServerTimeoutError

from utils.database_api.schemas.user import User

request_uri, first_secret_key, second_secret_key = getenv("REQUEST_ESP").split()


def set_post_json_dict(user_id: User.id, level: str) -> dict:
    return {
        "secret_key": level,
        "user_id": user_id
    }


async def send_first_level(user_id: int) -> dict:
    return await send_request_from_esp(set_post_json_dict(user_id=user_id, level=first_secret_key))


async def send_second_level(user_id: int) -> dict:
    return await send_request_from_esp(set_post_json_dict(user_id=user_id, level=second_secret_key))


async def send_request_from_esp(post_json_data: dict) -> dict:
    try:
        async with ClientSession() as session:
            async with session.post(url=request_uri, data=post_json_data) as response:
                return await response.json()
    except ClientConnectionError as client_connection_error:
        print(client_connection_error)
        return {
            'value': 0,
        }
    except ServerTimeoutError as server_error:
        print(server_error)
        return {
            'value': 0,
        }
