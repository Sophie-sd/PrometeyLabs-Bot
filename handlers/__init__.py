"""
Обробники повідомлень для PrometeyLabs Telegram Bot
"""

from .message_handlers import setup_message_handlers
from .command_handlers import setup_command_handlers
from .callback_handlers import setup_callback_handlers

__all__ = ['setup_message_handlers', 'setup_command_handlers', 'setup_callback_handlers']
