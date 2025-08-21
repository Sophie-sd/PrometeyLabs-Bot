"""
Налаштування логування для PrometeyLabs Telegram Bot
"""
import logging
import sys
from config import LOG_LEVEL, LOG_FORMAT

def setup_logging():
    """Налаштування системи логування"""
    try:
        # Валідація рівня логування
        log_level = LOG_LEVEL.upper()
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            print(f"⚠️  Невідомий рівень логування: {LOG_LEVEL}, використовую INFO")
            log_level = 'INFO'
        
        # Налаштування кореневого логера
        logging.basicConfig(
            level=getattr(logging, log_level),
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
        
        # Налаштування логера для SQLAlchemy
        sqlalchemy_logger = logging.getLogger('sqlalchemy')
        sqlalchemy_logger.setLevel(logging.WARNING)
        
        logger = logging.getLogger(__name__)
        logger.info(f"✅ Логування налаштовано на рівень {log_level}")
        
        return logger
        
    except Exception as e:
        print(f"❌ Помилка налаштування логування: {e}")
        # Fallback до базового логування
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
