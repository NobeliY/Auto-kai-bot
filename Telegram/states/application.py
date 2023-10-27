from aiogram.dispatcher.filters.state import State, StatesGroup


class ApplicationSubmission(StatesGroup):
    """
        Application fork
    """
    select_mode = State()
    user_id = State()
    user_initials = State()
    user_email = State()
    user_phone_number = State()
    user_academy_group = State()
    user_car_mark = State()
    user_state_number = State()
