from aiogram.dispatcher.filters.state import State, StatesGroup


class ApplicationSubmission(StatesGroup):
    """
        Ветка заявки
    """
    user_id = State()
    user_fully_name = State()
    user_email = State()
    user_academy_group = State()
    user_state_number = State()
