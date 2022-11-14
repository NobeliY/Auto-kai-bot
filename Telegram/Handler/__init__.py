# from .handlers import register_handlers
# from .handlers import dp
from .default.default import dp
from .default.start_command import dp
from .user.info import dp
from .user.open_command import dp
from .admin.admin_command import dp
from .admin.application_section import dp
from .admin.user_section import dp
from .application.application_command import dp

__all__ = ["dp"]
