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
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:////opt/render/project/src/data/bot_database.db')

# Перевірка наявності токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено в змінних середовища!")

# Перевірка наявності Google Sheets налаштувань
if not GOOGLE_SHEETS_CREDENTIALS:
    print("⚠️  GOOGLE_SHEETS_CREDENTIALS не налаштовано - Google Sheets функції будуть недоступні")
if not GOOGLE_SHEETS_ID:
    print("⚠️  GOOGLE_SHEETS_ID не налаштовано - Google Sheets функції будуть недоступні")

# Додаткові перевірки безпеки
def validate_config():
    """Валідація конфігурації"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не налаштовано!")
    
    if len(BOT_TOKEN) < 10:
        raise ValueError("BOT_TOKEN занадто короткий!")
    
    # Перевіряємо формат токена (повинен бути число:букви_цифри)
    if ':' not in BOT_TOKEN:
        raise ValueError("BOT_TOKEN має неправильний формат!")
    
    # Перевіряємо DATABASE_URL
    if DATABASE_URL.startswith('sqlite'):
        print("⚠️  Використовується SQLite - рекомендується PostgreSQL для production")
    
    print("✅ Конфігурація валідна")

# Запускаємо валідацію
if __name__ == "__main__":
    validate_config()
else:
    # Тихо валідуємо при імпорті
    try:
        validate_config()
    except Exception as e:
        print(f"⚠️  Помилка валідації: {e}")
