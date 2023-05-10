import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ContentType

from Data import __all_states__
from Handler.admin.admin_command import (
    call_admin_panel, users_info, set_add_menu,
    set_remove_menu, show_fully_information, preview_step,
    # show_applications
)
from Handler.admin.application_section import (
    auto_add_by_application, manual_add_user,
    get_application_from_begin, next_application, approve_application,
    submit_reject_application, reject_application, get_application_from_end, approve_student_level_from_application,
    approve_application_from_list, start_manual_add, get_user_id_from_manual_add, get_user_initials_from_manual_add,
    get_user_email_from_manual_add, get_user_phone_number_from_manual_add, get_academy_group_from_manual_add,
    get_user_state_number_from_manual_add, get_user_access_from_manual_add, approve_manual_add_user
)
from Handler.admin.change_ap_command import get_change_application, get_change_application_from_begin, \
    get_change_application_from_end, next_change_application, approve_change_application, \
    reject_change_application, confirm_reject, confirm_approve_change_application, close_change_application, \
    cancel_approve_change_application
from Handler.admin.send_messages import get_send_message_menu, close_send_message_menu, get_group_set_to_send, \
    send_message_choice, approve_send_message
from Handler.admin.user_section import (
    delete_user_by_initials, delete_all_from_group,
    delete_user_by_initials_searched, send_all_searched_users_for_delete,
    delete_user_question, delete_user, decline_delete_user, get_group_for_delete, accept_delete_group,
    decline_delete_group
)
from Handler.application.application_command import (
    set_application, application_submission_initials, application_submission_email,
    application_submission_phone, application_submission_academy_group, application_submission_state_number,
    select_application_mode
)
from Handler.default.start_command import start
from Handler.help.help_fork import send_help_fork
from Handler.user.info import (
    change_user_info, get_free_positions, get_user_info, close_user_info, change_initials, change_email,
    change_phone_number, change_group, change_state_number, accept_changes, cancel_changes, agree_changes,
    get_change_initials, get_change_email, get_change_group, get_change_phone, get_change_state_number, close_info,
    preview_step_info
)
from Handler.user.open_command import (
    open_from_all_registered_users, open_first_level_from_employee,
    open_second_level_from_employee
)
from states import UserState, ApplicationSubmission, Admins, ManualAdd, UserChanges


def register_handlers(dp: Dispatcher):
    logging.warning(f"Register handlers: {dp}")
    """
        Start Command
    """
    dp.register_message_handler(start, Command("start"), state="*")
    dp.register_message_handler(application_submission_initials, state=ApplicationSubmission.user_initials)
    dp.register_message_handler(application_submission_email, state=ApplicationSubmission.user_email)
    dp.register_message_handler(application_submission_phone, state=ApplicationSubmission.user_phone_number)
    dp.register_message_handler(application_submission_academy_group, state=ApplicationSubmission.user_academy_group)
    dp.register_message_handler(application_submission_state_number, state=ApplicationSubmission.user_state_number)

    """
        Application
    """
    dp.register_message_handler(select_application_mode, Command("application"), state="*")
    dp.register_callback_query_handler(set_application, Text(equals="old_type"),
                                       state=ApplicationSubmission.select_mode)
    # dp.register_message_handler(application_from_web_app, content_types='web_app_data')
    # dp.register_message_handler(application_from_web_app, content_types=ContentType.WEB_APP_DATA)

    """
        INFO
    """
    dp.register_message_handler(get_free_positions, Text(equals="свободные места", ignore_case=True),
                                state=__all_states__)
    dp.register_callback_query_handler(change_user_info, Text(equals="change_info_menu"),
                                       state=__all_states__)

    """
    INFO -> Sector change application
    """
    dp.register_message_handler(get_user_info, Text(equals="информация о себе", ignore_case=True),
                                state=__all_states__)
    dp.register_callback_query_handler(close_user_info, Text(equals="close_info"),
                                       state=__all_states__)
    dp.register_callback_query_handler(change_user_info, Text(equals="change_info_menu"),
                                       state=__all_states__)
    dp.register_callback_query_handler(change_initials, Text(equals="change_initials"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(change_email, Text(equals="change_email"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(change_phone_number, Text(equals="change_phone"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(change_group, Text(equals="change_group"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(change_state_number, Text(equals="change_state_number"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(accept_changes, Text(equals="finish_changes"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(cancel_changes, Text(equals="cancel_changes"),
                                       state=UserChanges.change_menu)

    dp.register_callback_query_handler(agree_changes, Text(equals="agree_changes"),
                                       state=UserChanges.change_menu)

    dp.register_message_handler(get_change_initials, state=UserChanges.change_initials)
    dp.register_message_handler(get_change_email, state=UserChanges.change_email)
    dp.register_message_handler(get_change_phone, state=UserChanges.change_phone)
    dp.register_message_handler(get_change_group, state=UserChanges.change_group)
    dp.register_message_handler(get_change_state_number, state=UserChanges.change_state_number)
    dp.register_callback_query_handler(close_info, Text(equals="close_info"),
                                       state=UserChanges.change_menu)
    dp.register_callback_query_handler(preview_step_info, Text(equals="preview_step"),
                                       state=UserChanges.all_states)

    """
        Open Command
    """
    dp.register_message_handler(open_from_all_registered_users, Text(equals="открыть", ignore_case=True),
                                state=UserState.all_states)
    dp.register_message_handler(open_first_level_from_employee, Text(equals="открыть шлагбаум", ignore_case=True),
                                state=__all_states__)
    dp.register_message_handler(open_second_level_from_employee, Text(equals="открыть железные ворота",
                                                                      ignore_case=True),
                                state=__all_states__)

    """
        Admin Command
    """
    dp.register_message_handler(call_admin_panel, Text(equals="панель для администратора", ignore_case=True),
                                state=__all_states__)
    dp.register_callback_query_handler(users_info, Text(equals="users_info"),
                                       state=Admins.main_state)
    dp.register_callback_query_handler(set_add_menu, Text(equals="user_add_menu"),
                                       state=Admins.main_state)
    dp.register_callback_query_handler(set_remove_menu, Text(equals="user_remove_menu"),
                                       state=Admins.main_state)
    # dp.register_callback_query_handler(show_applications, Text(equals="show_applications"),
    #                                    state=Admins.main_state)
    dp.register_callback_query_handler(show_fully_information, Text(equals="show_fully_information_from_db"),
                                       state=Admins.show_db_state)
    dp.register_callback_query_handler(preview_step, Text(equals="preview_step"),
                                       state=Admins.all_states)

    """
        Admin -> Change Application Section
    """
    dp.register_callback_query_handler(get_change_application, Text(equals="show_applications"),
                                       state=Admins.all_states)
    dp.register_callback_query_handler(get_change_application_from_begin, Text(equals="start_from_begin"),
                                       state=Admins.show_change_application)
    dp.register_callback_query_handler(get_change_application_from_end, Text(equals="start_from_end"),
                                       state=Admins.show_change_application)
    dp.register_callback_query_handler(next_change_application, Text(equals="next_application"),
                                       state=Admins.show_change_application)
    dp.register_callback_query_handler(approve_change_application, Text(equals="approve_application"),
                                       state=Admins.show_change_application)
    dp.register_callback_query_handler(confirm_approve_change_application, Text(equals="approve_level_application"),
                                       state=Admins.show_selected_change_application)
    dp.register_callback_query_handler(cancel_approve_change_application, Text(equals="preview_step"),
                                       state=Admins.show_selected_change_application)
    dp.register_callback_query_handler(reject_change_application, Text(equals="submit_reject_application"),
                                       state=Admins.show_change_application)
    dp.register_callback_query_handler(confirm_reject, Text(equals="reject_application"),
                                       state=Admins.show_change_application)
    dp.register_callback_query_handler(close_change_application, Text(equals="preview_step"),
                                       state=Admins.show_change_application)

    """
        Admin Application Section
    """
    dp.register_callback_query_handler(auto_add_by_application, Text(equals="auto_add_by_application"),
                                       state=Admins.add_menu_state)
    dp.register_callback_query_handler(get_application_from_begin, Text(equals="start_from_begin"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(next_application, Text(equals="next_application"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(approve_application_from_list, Text(equals="approve_application"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(submit_reject_application, Text(equals="submit_reject_application"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(reject_application, Text(equals="reject_application"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(get_application_from_end, Text(equals="start_from_end"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(approve_student_level_from_application,
                                       Text(equals=['student', 'student_plus',
                                                    'teacher', 'employee',
                                                    'administrator']),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(approve_application, Text(equals="approve_level_application"),
                                       state=Admins.auto_add_state)
    dp.register_callback_query_handler(manual_add_user, Text(equals="manual_add"),
                                       state=Admins.add_menu_state)
    dp.register_callback_query_handler(start_manual_add, Text(equals="start_manual_add"),
                                       state=Admins.manual_add_state)
    dp.register_message_handler(get_user_id_from_manual_add, state=ManualAdd.id)
    dp.register_message_handler(get_user_initials_from_manual_add, state=ManualAdd.initials)
    dp.register_message_handler(get_user_email_from_manual_add, state=ManualAdd.email)
    dp.register_message_handler(get_user_phone_number_from_manual_add, state=ManualAdd.phone_number)
    dp.register_message_handler(get_academy_group_from_manual_add, state=ManualAdd.academy_group)
    dp.register_message_handler(get_user_state_number_from_manual_add, state=ManualAdd.state_number)
    dp.register_callback_query_handler(get_user_access_from_manual_add,
                                       Text(equals=["student", "student_plus",
                                                    "teacher", "employee",
                                                    "administrator"]),
                                       state=ManualAdd.level)
    dp.register_callback_query_handler(approve_manual_add_user, Text(equals="approve_level_application"),
                                       state=ManualAdd.approve)

    """
        Admin User Section
    """
    dp.register_callback_query_handler(delete_user_by_initials, Text(equals="delete_by_initials"),
                                       state=Admins.delete_menu_state)
    dp.register_message_handler(delete_user_by_initials_searched, content_types=ContentType.TEXT,
                                state=Admins.searched_user_delete_state)
    dp.register_callback_query_handler(send_all_searched_users_for_delete, Text(equals="show_fully_searched_users"),
                                       state=Admins.searched_user_delete_state)
    dp.register_callback_query_handler(delete_user_question, Text(equals="selected_user_for_delete"),
                                       state=Admins.searched_user_delete_state)
    dp.register_callback_query_handler(delete_user, Text(equals="accept_delete"),
                                       state=Admins.searched_user_delete_state)
    dp.register_callback_query_handler(decline_delete_user, Text(equals="decline_delete"),
                                       state=Admins.searched_user_delete_state)
    dp.register_callback_query_handler(delete_all_from_group, Text(equals="delete_all_group"),
                                       state=Admins.delete_menu_state)
    dp.register_message_handler(get_group_for_delete, content_types=ContentType.TEXT,
                                state=Admins.delete_all_group_state)
    dp.register_callback_query_handler(accept_delete_group, Text(equals="accept_delete"),
                                       state=Admins.delete_all_group_state)
    dp.register_callback_query_handler(decline_delete_group, Text(equals="decline_delete"),
                                       state=Admins.delete_all_group_state)

    """
    Admin -> Send Message from users group
    """
    dp.register_message_handler(get_send_message_menu, Text(equals="отправить сообщение", ignore_case=True),
                                state="*")

    dp.register_callback_query_handler(close_send_message_menu, Text(equals="close_send"),
                                       state=Admins.send_message_state)
    dp.register_callback_query_handler(get_group_set_to_send,
                                       Text(equals=["send_students", "send_employees",
                                                    "send_admins", "send_all"]),
                                       state=Admins.send_message_state)
    dp.register_message_handler(send_message_choice, state=Admins.send_message_state)
    dp.register_callback_query_handler(approve_send_message, Text(equals="approve_send_message"),
                                       state=Admins.send_message_state)

    """
        Help Fork
    """
    dp.register_message_handler(send_help_fork, Command('help'), state='*')
