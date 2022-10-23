import datetime
from os import getenv
import requests

from utils.database_api.schemas.user import User

request_uri, first_secret_key, second_secret_key = getenv("REQUEST_ESP").split()


# first_secret_key = getenv("FIRST_SECRET_KEY")
# second_secret_key = getenv("SECOND_SECRET_KEY")
# request_uri = getenv("REQUEST_ESP_URI")


async def set_post_json_dict(user_id: User.id, level: str) -> dict:
    return {
        "secret_key": level,
        "user_id": user_id
    }


async def send_first_level(user: User, object_title: str) -> bool | None:
    request_full_uri = await request_init(object_title)
    post_json_data = await set_post_json_dict(user_id=user.id, level=first_secret_key)
    if request_full_uri is None:
        return
    request_ = requests.post(url=request_full_uri, json=post_json_data)
    if request_.status_code != 200:
        print(f"User ID: {user.id}| Trying send first Level: Preview status code: {request_.status_code}")
        await send_first_level(user=user, object_title=object_title)
    return True


async def send_second_level(user: User, object_title: str) -> bool | None:
    request_full_uri = await request_init(object_title)
    post_json_data = await set_post_json_dict(user_id=user.id, level=second_secret_key)
    if request_full_uri is None:
        return
    request_ = requests.post(url=request_full_uri, json=post_json_data)
    if request_.status_code != 200:
        print(f"User ID: {user.id}| Trying send second Level: Preview status code: {request_.status_code}")
        await send_second_level(user=user, object_title=object_title)
    return True


async def request_init(object_title: str) -> str | None:
    if object_title.lower() == "открыть 1 уровень" or "открыть":
        return f"{request_uri}/{first_secret_key}"
    else:
        return f"{request_uri}/{second_secret_key}" if object_title.lower() == "открыть 2 уровень" else None
