"""
Обробники повідомлень для PrometeyLabs Telegram Bot
"""

from .message_handlers import setup_message_handlers
from .command_handlers import setup_command_handlers
from .callback_handlers import setup_callback_handlers
from .menu_utils import (
    show_menu_for_user, show_new_client_menu, show_client_menu, show_admin_menu
)

__all__ = [
    'setup_message_handlers', 
    'setup_command_handlers', 
    'setup_callback_handlers',
    'show_menu_for_user',
    'show_new_client_menu',
    'show_client_menu',
    'show_admin_menu'
]
