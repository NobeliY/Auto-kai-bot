from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    admin_all_send = State()
