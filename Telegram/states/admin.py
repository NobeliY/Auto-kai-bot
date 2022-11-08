from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    """
        Ветка пользователя
    """
    main_state = State()
    show_db_state = State()

    add_menu_state = State()
    auto_add_state = State()
    manual_add_state = State()

    delete_menu_state = State()
    searched_user_delete_state = State()
    delete_all_group_state = State()

    show_applications_state = State()
    all_applications_state = State()
