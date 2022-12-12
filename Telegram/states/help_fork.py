from aiogram.dispatcher.filters.state import State, StatesGroup


class HelpFork(StatesGroup):
    """
        Help fork
    """
    menu_help = State()
    help_back = State()
