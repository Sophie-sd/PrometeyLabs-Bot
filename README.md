# PrometeyLabs Telegram Bot

Офіційний Telegram-бот для PrometeyLabs з особистим кабінетом клієнта, інтеграцією з Google Таблицями та адмін-панеллю.

## 🚀 Швидкий старт

### Локальний запуск:
1. Клонуйте репозиторій:
```bash
git clone https://github.com/your-username/prometeylabs_telegram_bot.git
cd prometeylabs_telegram_bot
```

2. Створіть віртуальне середовище:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate     # Windows
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

4. Створіть файл `.env` на основі `.env.example`:
```bash
cp .env.example .env
# Відредагуйте .env та додайте ваш BOT_TOKEN
```

5. Запустіть бота:
```bash
python main.py
```

### Деплой на Render:
1. Підключіть GitHub репозиторій до Render
2. Налаштуйте змінні середовища:
   - `BOT_TOKEN` - токен вашого Telegram бота
   - `GOOGLE_SHEETS_CREDENTIALS` - JSON файл з креденшлами Google
   - `GOOGLE_SHEETS_ID` - ID Google таблиці
   - `LOG_LEVEL` - рівень логування (INFO, DEBUG, ERROR)
3. Автоматичний деплой при push в main гілку

### Веб-хуки після деплою:
1. **Встановіть веб-хук:**
   ```
   https://your-app.onrender.com/set_webhook?url=https://your-app.onrender.com
   ```

2. **Перевірте статус:**
   ```
   https://your-app.onrender.com/bot_info
   ```

3. **Видаліть веб-хук (якщо потрібно):**
   ```
   https://your-app.onrender.com/delete_webhook
   ```

## 📁 Структура проекту

```
prometeylabs_telegram_bot/
├── main.py                 # Головний файл бота (локальний запуск)
├── web_server.py           # Веб-сервер для Render
├── config.py               # Конфігурація та змінні середовища
├── database.py             # Моделі бази даних SQLAlchemy
├── google_sheets.py        # Інтеграція з Google Sheets
├── handlers/               # Обробники повідомлень
│   ├── command_handlers.py # Обробники команд (/start, /help)
│   ├── message_handlers.py # Обробники текстових повідомлень
│   ├── callback_handlers.py # Обробники inline кнопок
│   └── menu_utils.py       # Спільні утиліти для меню
├── utils/                  # Допоміжні функції
│   └── logger.py           # Налаштування логування
├── requirements.txt        # Python залежності
├── render.yaml            # Конфігурація для Render
├── Procfile               # Конфігурація для Render
└── README.md              # Документація
```

## 🎯 Функціональність

### Для клієнтів:
- 🛍️ **Послуги**: Замовлення сайтів, реклами, AI-відео, ведення соцмереж
- 🎓 **Навчання**: Курси з IT, маркетингу та AI
- 📊 **Особистий кабінет**: Перегляд проектів, оплат, статистики
- 📎 **Документи**: Доступ до договорів та актів

### Для адміністраторів:
- 👥 **Управління клієнтами**: Перегляд та редагування інформації
- 📂 **Звіти**: Інтеграція з Google Sheets
- 🔔 **Сповіщення**: Push-повідомлення клієнтам
- 📜 **Підписки**: Моніторинг активних підписок

## 🔧 Технології

- **Python 3.9+** - основна мова програмування
- **python-telegram-bot v20** - Telegram Bot API
- **SQLAlchemy 2.0** - ORM для бази даних
- **SQLite/PostgreSQL** - база даних
- **Google Sheets API** - інтеграція з таблицями
- **python-dotenv** - управління змінними середовища

## 🌐 Деплой

### Render.com (рекомендовано):
- Автоматичний деплой з GitHub
- Безкоштовний план доступний
- Підтримка PostgreSQL

### Heroku:
- Використовуйте Procfile
- Налаштуйте змінні середовища
- Підключіть базу даних

## 📖 Документація

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot v20](https://python-telegram-bot.readthedocs.io/en/v20.0/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Google Sheets API](https://developers.google.com/sheets/api)

## 🤝 Внесок

1. Форкніть репозиторій
2. Створіть feature гілку (`git checkout -b feature/amazing-feature`)
3. Зробіть коміт (`git commit -m 'Add amazing feature'`)
4. Запушіть гілку (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 📄 Ліцензія

Цей проект розповсюджується під ліцензією MIT. Дивіться файл `LICENSE` для деталей.

## 📞 Підтримка

Якщо у вас є питання або проблеми:
- Створіть Issue в GitHub
- Зв'яжіться з командою PrometeyLabs
- Email: info@prometeylabs.com
