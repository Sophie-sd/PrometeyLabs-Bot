# PrometeyLabs Telegram Bot

Офіційний Telegram-бот для PrometeyLabs з особистим кабінетом клієнта, інтеграцією з Google Таблицями та адмін-панеллю.

## 🚀 Швидкий старт

### Локальний запуск:
1. Клонуйте репозиторій:
```bash
git clone https://github.com/Sophie-sd/PrometeyLabs-Bot.git
cd PrometeyLabs-Bot
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

4. Створіть файл `.env`:
```bash
# Створіть .env файл з наступним вмістом:
BOT_TOKEN=your_telegram_bot_token_here
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///bot_database.db
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials.json
GOOGLE_SHEETS_ID=your_spreadsheet_id
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
   ```bash
   python setup_webhook.py set
   ```

2. **Перевірте статус:**
   ```bash
   python test_bot_status.py
   ```

3. **Keep-alive для free tier:**
   ```bash
   python keep_alive.py
   ```

4. **Ручна перевірка:**
   - Health check: `https://your-app.onrender.com/`
   - Bot info: `https://your-app.onrender.com/bot_info`

## 📁 Структура проекту

```
PrometeyLabs-Bot/
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
├── setup_webhook.py       # Скрипт для встановлення webhook
├── test_bot_status.py     # Діагностика бота
├── keep_alive.py          # Keep-alive скрипт для Render
├── BOT_TROUBLESHOOTING.md # Інструкція з виправлення проблем
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
- **python-telegram-bot 20.7** - Telegram Bot API
- **Flask** - веб-фреймворк для Render
- **SQLAlchemy** - ORM для бази даних
- **PostgreSQL** - основна база даних (production)
- **Google Sheets API** - інтеграція з таблицями
- **Render** - хостинг платформа

## 🚨 Виправлення проблем

Якщо бот не працює, дивіться детальну інструкцію в [BOT_TROUBLESHOOTING.md](BOT_TROUBLESHOOTING.md)

### Швидкі команди:
```bash
# Діагностика
python test_bot_status.py

# Встановлення webhook
python setup_webhook.py set

# Keep-alive
python keep_alive.py
```

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
