import os
from datetime import time
from pathlib import Path
from dotenv import load_dotenv

from states import UserState, Admins, UserChanges

load_dotenv()

# Basic Configuration
admins = [int(admin_id) for admin_id in os.getenv('ADMIN_ID_LIST').split(' ')]
BOT_TOKEN = os.getenv('BOT_TOKEN_AUTO')
TIME_RANGE = [time(6, 0), time(23, 0)]
USER_CSV_PATH = Path('Data/users.csv')
LOGGING_LEVEL = os.getenv("LEVEL")
WEB_APP_URL = os.getenv("WEB_APP_URL")
__all_states__ = UserState.all_states + Admins.all_states


# PostgreSQL connect configuration
PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DATABASE = os.getenv('PG_DATABASE')

POSTGRES_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'


def get_postgres_uri():
    return POSTGRES_URL


# SMTP Server connect configuration
SMTP_SERVER = os.getenv("EMAIL_SERVER")
SMTP_PORT = os.getenv("EMAIL_PORT")
SMTP_FROM_LOGIN = os.getenv("EMAIL_LOGIN")
SMTP_FROM_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_TO = os.getenv("SMTP_TO")
