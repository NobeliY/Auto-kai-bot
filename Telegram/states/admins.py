from aiogram.dispatcher.filters.state import State, StatesGroup


class Admins(StatesGroup):
    """
        Admin fork
    """
    main_state = State()
    show_db_state = State()
    show_fully_state = State()

    add_menu_state = State()
    auto_add_state = State()
    manual_add_state = State()

    delete_menu_state = State()
    searched_user_delete_state = State()
    delete_all_group_state = State()

    show_applications_state = State()
    all_applications_state = State()


class ManualAdd(StatesGroup):
    """
        Admin manual add user fork
    """
    id = State()
    initials = State()
    email = State()
    phone_number = State()
    academy_group = State()
    state_number = State()
    level = State()
    approve = State()

