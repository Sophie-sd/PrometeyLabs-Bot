"""
Налаштування логування для PrometeyLabs Telegram Bot
"""
import logging
import sys
from config import LOG_LEVEL, LOG_FORMAT

def setup_logging():
    """Налаштування системи логування"""
    # Налаштування кореневого логера
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
            # Файлове логування тільки для локальної розробки
            # logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )
    
    # Налаштування логера для telegram
    telegram_logger = logging.getLogger('telegram')
    telegram_logger.setLevel(logging.WARNING)
    
    # Налаштування логера для httpx
    httpx_logger = logging.getLogger('httpx')
    httpx_logger.setLevel(logging.WARNING)
    
    # Налаштування логера для urllib3
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Логування налаштовано на рівень {LOG_LEVEL}")
    
    return logger
