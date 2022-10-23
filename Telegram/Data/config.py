import os
from datetime import time

admins = [int(admin_id) for admin_id in os.getenv('ADMIN_ID').split(' ')]

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DATABASE = os.getenv('PG_DATABASE')

POSTGRES_URL = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'


def get_postgres_uri():
    return POSTGRES_URL


TIME_RANGE = [time(6, 0), time(23, 0)]
