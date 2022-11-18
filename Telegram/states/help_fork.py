from aiogram.dispatcher.filters.state import State, StatesGroup


class HelpFork(StatesGroup):
    """
        Ветка помощи
    """
    menu_help = State()
    help_back = State()
