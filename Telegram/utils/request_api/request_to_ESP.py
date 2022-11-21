
from os import getenv
import requests

from utils.database_api.schemas.user import User

request_uri, first_secret_key, second_secret_key = getenv("REQUEST_ESP").split()


async def set_post_json_dict(user_id: User.id, level: str) -> dict:
    return {
        "secret_key": level,
        "user_id": user_id
    }


async def send_first_level(user_id: int) -> dict:
    post_json_data = await set_post_json_dict(user_id=user_id, level=first_secret_key)
    request_ = requests.post(url=request_uri, data=post_json_data)
    # if request_.status_code != 200:
    #     print(f"User ID: {user.id}| Trying send first Level: Preview status code: {request_.status_code}")
    #     await send_first_level(user=user)
    return request_.json()


async def send_second_level(user_id: int) -> dict:
    post_json_data = await set_post_json_dict(user_id=user_id, level=second_secret_key)
    request_ = requests.post(url=request_uri, json=post_json_data)
    # if request_.status_code != 200:
    #     print(f"User ID: {user.id}| Trying send second Level: Preview status code: {request_.status_code}")
    #     await send_second_level(user=user)
    return request_.json()
