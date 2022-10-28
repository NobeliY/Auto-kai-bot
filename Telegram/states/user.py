from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """
        Ветка пользователя
    """
    in_active = State()
