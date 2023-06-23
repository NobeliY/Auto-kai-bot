from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """
        User fork
    """
    in_active = State()
    is_admin = State()
    is_guest = State()


class UserChanges(StatesGroup):
    change_menu = State()
    user_id = State()
    change_initials = State()
    change_email = State()
    change_phone = State()
    change_group = State()
    change_state_number = State()
    accept = State()
