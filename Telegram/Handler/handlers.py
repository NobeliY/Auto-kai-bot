from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command

from app import dp

from Handler.admin.admin_command import call_admin_panel, users_info, set_add_menu, set_remove_menu, show_applications, \
    auto_add_by_application, manual_add_user, delete_user_by_initials, delete_all_from_group
from Handler.application import set_application, application_submission_initials, application_submission_email, \
    application_submission_phone, application_submission_academy_group, application_submission_state_number
from Handler.user.info import get_user_info, get_free_positions
from Handler.user.open_command import open_from_all_registered_users, open_first_level_from_employee, \
    open_second_level_from_employee
from states import UserState, ApplicationSubmission


def register_handlers(dp: Dispatcher):
    print("Start registering handlers")
    # Start command
    dp.register_message_handler(Command("start"), state="*")

    # Employee commands
    dp.register_message_handler(open_from_all_registered_users, Text(equals="открыть", ignore_case=True),
                                state=UserState.all_states)
    dp.register_message_handler(open_first_level_from_employee, Text(equals="Открыть 1 уровень", ignore_case=True),
                                state=UserState.all_states)
    dp.register_message_handler(open_second_level_from_employee, Text(equals="Открыть 2 уровень", ignore_case=True),
                                state=UserState.all_states)

    # User info commands
    dp.register_message_handler(get_user_info, Text(equals="информация о себе", ignore_case=True),
                                state=UserState.all_states)
    dp.register_message_handler(get_free_positions, Text(equals="свободные места", ignore_case=True),
                                state=UserState.all_states)

    # Admin commands
    dp.register_message_handler(call_admin_panel, Text(equals="панель для администратора", ignore_case=True),
                                state=UserState.all_states)
    dp.register_callback_query_handler(users_info, Text(equals="users_info", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(set_add_menu, Text(equals="user_add_menu", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(set_remove_menu, Text(equals="user_remove_menu", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(show_applications, Text(equals="show_applications", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(auto_add_by_application,
                                       Text(equals="auto_add_by_application", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(manual_add_user, Text(equals="manual_add", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(delete_user_by_initials, Text(equals="delete_by_initials", ignore_case=True),
                                       state=UserState.is_admin)
    dp.register_callback_query_handler(delete_all_from_group, Text(equals="delete_all_group", ignore_case=True),
                                       state=UserState.is_admin)

    # Application commands
    dp.register_message_handler(set_application, Command("application"), state="*")
    dp.register_message_handler(application_submission_initials, state=ApplicationSubmission.user_initials)
    dp.register_message_handler(application_submission_email, state=ApplicationSubmission.user_email)
    dp.register_message_handler(application_submission_phone, state=ApplicationSubmission.user_phone_number)
    dp.register_message_handler(application_submission_academy_group, state=ApplicationSubmission.user_academy_group)
    dp.register_message_handler(application_submission_state_number, state=ApplicationSubmission.user_state_number)
