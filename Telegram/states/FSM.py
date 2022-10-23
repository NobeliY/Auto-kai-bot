from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """
        Ветка пользователя
    """
    in_active = State()


class ApplicationSubmission(StatesGroup):
    """
        Ветка заявки
    """
    user_id = State()
    user_fully_name = State()
    user_email = State()
    user_academy_group = State()
    user_state_number = State()


class Admin(StatesGroup):
    admin_all_send = State()


class HelpFork(StatesGroup):
    """
        Ветка помощи
    """
    menu_help = State()
    help_back = State()
