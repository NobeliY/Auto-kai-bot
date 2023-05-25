import os
from datetime import time, datetime
from pathlib import Path

from dotenv import load_dotenv

from states import UserState, Admins

load_dotenv()

# Basic Configuration
admins = [int(admin_id) for admin_id in os.getenv('ADMIN_ID_LIST').split(' ')]
BOT_TOKEN = os.getenv('BOT_TOKEN_AUTO')
TIME_RANGE = [time(6, 0), time(23, 0)]
USER_CSV_PATH = Path('Data/users.csv')
USER_XLSX_PATH = Path('Data/users.xlsx')
LOGGING_LEVEL = os.getenv("LEVEL")
LOGGING_PATH = f"{os.getcwd()}/logs"
print(LOGGING_PATH)
LOGGING_FILE = os.getenv('LOG_FILENAME')
WEB_APP_URL = os.getenv("WEB_APP_URL")
__all_states__ = UserState.all_states + Admins.all_states


# PostgreSQL connect configuration
PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DATABASE = os.getenv('PG_DATABASE')

POSTGRES_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'


def check_log_dir() -> None:
    if not os.path.exists(LOGGING_PATH):
        os.makedirs("logs", exist_ok=True)


def get_postgres_uri() -> str:
    return POSTGRES_URL


# SMTP Server connect configuration
SMTP_SERVER = os.getenv("EMAIL_SERVER")
SMTP_PORT = os.getenv("EMAIL_PORT")
SMTP_FROM_LOGIN = os.getenv("EMAIL_LOGIN")
SMTP_FROM_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_TO = os.getenv("SMTP_TO")
