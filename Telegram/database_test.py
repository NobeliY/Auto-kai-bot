import asyncio
import json

from Data import POSTGRES_URL
from utils.database_api import quick_commands as commands
from utils.database_api.database_gino import database


async def database_test():
    await database.set_bind(POSTGRES_URL)
    await database.gino.drop_all()
    await database.gino.create_all()

    await commands.add_user(
        user_id=834865678,
        initials='Гильметдинов Инсаф Нафисович',
        email='nobeliylord@gmail.com',
        phone_number='+79083385215',
        group='20-00',
        state_number='A363МА|116',
        access='A'
    )
    await commands.add_user(
        user_id=665722525,
        initials='Астафьев Олег Валерьевич',
        email='nrd@gmail.com',
        phone_number='+79172993502',
        group='ивц',
        state_number='А123АА|116',
        access='A'
    )

    # await commands.add_application(user_id=2, initials='hi de', email='hi_de@er.er',
    #                                group='232-22', phone_number="8989898989", state_number='a123aa|123')
    # await commands.add_application(user_id=3, initials='shi de', email='hi_de@easdr.er',
    #                                group='23-222', phone_number="8989898989", state_number='a123ta|123')
    # await commands.add_application(user_id=4, initials='haas de', email='hiasd_de@er.er',
    #                                group='2-3222', phone_number="8989898989", state_number='a123sa|123')
    # await commands.add_application(user_id=5, initials='hi dade', email='hadi_de@er.er',
    #                                group='2322-2', phone_number="8989898989", state_number='a123wa|123')

    # with open("Data/Refactored_DB.json", "r", encoding="utf-8") as file:
    #     json_dict = json.load(file)
    #     for access_level, user_list in json_dict.items():
    #         for user in user_list:
    #             await commands.add_user(
    #                 user_id=int(user['user_id']),
    #                 initials=user['initials'],
    #                 phone_number=user['phone_number'],
    #                 group=user['group'],
    #                 state_number=user['state_number'],
    #
    #                 access='S' if access_level == 'Студент'
    #                 else 'T' if access_level == 'Преподаватель'
    #                 else 'E',
    #                 email=""
    #             )


loop = asyncio.get_event_loop().run_until_complete(database_test())
