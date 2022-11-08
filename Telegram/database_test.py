import asyncio
import re

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
        access='T'
    )
    await commands.add_user(
        user_id=541842024,
        initials='Шигапов Руслан Ринатович',
        email='test@gmail.com',
        phone_number='+79172617052',
        group='кмт',
        state_number='В847КР|716',
        access='S'
    )
    await commands.add_user(
        user_id=931611739,
        initials='Мокшин Владимир Васильевич',
        email='test@gmail.com',
        phone_number='+79270322877',
        group='Преподаватель',
        state_number='В885ТЕ|716',
        access='T'
    )

    await commands.add_application(user_id=2, initials='hi de', email='hi_de@er.er',
                                   group='232-22', phone_number="8989898989", state_number='a123aa|123')
    await commands.add_application(user_id=3, initials='shi de', email='hi_de@easdr.er',
                                   group='23-222', phone_number="8989898989", state_number='a123ta|123')
    await commands.add_application(user_id=4, initials='hasdi de', email='hiasd_de@er.er',
                                   group='2-3222', phone_number="8989898989", state_number='a123sa|123')
    await commands.add_application(user_id=5, initials='hi dade', email='hadi_de@er.er',
                                   group='2322-2', phone_number="8989898989", state_number='a123wa|123')

    users = await commands.get_users_info(834865678)
    print([user.group for user in users])

    print(sum([1 if re.findall(r"\d-\d", user.group) else 0 for user in users]))

    print("Applications test")
    applications = await commands.get_count_of_applications(834865678)
    print(applications)


loop = asyncio.get_event_loop().run_until_complete(database_test())
# asyncio.run(database_test())
