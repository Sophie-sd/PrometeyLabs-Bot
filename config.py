"""
Конфігурація для PrometeyLabs Telegram Bot
"""
import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Налаштування бота
BOT_NAME = "PrometeyLabs Bot"
BOT_DESCRIPTION = "Офіційний бот PrometeyLabs з особистим кабінетом"

# Google Sheets налаштування
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')

# Налаштування логування
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Налаштування бази даних
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_database.db')

# Перевірка наявності токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено в змінних середовища!")
