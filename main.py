"""
Головний файл PrometeyLabs Telegram Bot
"""
import logging
import sys
from telegram.ext import Application

from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION
from handlers import setup_command_handlers, setup_message_handlers, setup_callback_handlers
from utils.logger import setup_logging
from database import create_tables

# Налаштування логування
logger = setup_logging()

async def error_handler(update, context):
    """Обробник помилок"""
    try:
        if update and update.effective_user:
            user_id = update.effective_user.id
            username = update.effective_user.username or "Unknown"
            logger.error(f"Помилка при обробці оновлення від користувача {user_id} (@{username}): {context.error}")
        else:
            logger.error(f"Помилка при обробці оновлення: {context.error}")
    except Exception as e:
        logger.error(f"Помилка в error_handler: {e}")

def main():
    """Головна функція бота"""
    logger.info("Запуск PrometeyLabs Telegram Bot...")
    
    # Створення таблиць бази даних
    try:
        create_tables()
        logger.info("База даних створена/підключена успішно")
    except Exception as e:
        logger.error(f"Помилка при створенні бази даних: {e}")
        return
    
    # Створення застосунку
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Налаштування обробників
    setup_command_handlers(application)
    setup_message_handlers(application)
    setup_callback_handlers(application)
    
    # Налаштування обробника помилок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info(f"Бот {BOT_NAME} запущений успішно!")
    logger.info(f"Опис: {BOT_DESCRIPTION}")
    
    # Запуск в режимі polling (синхронно для v20)
    application.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот зупинено користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
        sys.exit(1)
