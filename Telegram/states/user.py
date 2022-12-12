from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """
        User fork
    """
    in_active = State()
    is_admin = State()
