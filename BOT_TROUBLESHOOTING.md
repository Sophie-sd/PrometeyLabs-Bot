# 🔧 Виправлення проблем PrometeyLabs Telegram Bot

## 🚨 Поточна проблема: Бот не відповідає

### Причина:
- **Render сервіс "спить"** через неактивність (free tier)
- Webhook встановлено, але сервіс недоступний
- Telegram не може доставити повідомлення

## 🚀 Швидке виправлення:

### 1. Перезапустіть сервіс на Render:
```
1. Зайдіть на https://dashboard.render.com
2. Знайдіть "prometeylabs-telegram-bot"
3. Натисніть "Manual Deploy" або "Restart"
4. Дочекайтесь завершення деплою
```

### 2. Перевірте статус:
```bash
python3 test_bot_status.py
```

### 3. Якщо webhook не встановлено:
```bash
python3 setup_webhook.py set
```

## 🔄 Довгострокове рішення:

### Keep-alive скрипт:
```bash
# Встановіть залежності
pip install schedule

# Запустіть keep-alive (тримає сервіс активним)
python3 keep_alive.py
```

### Або використовуйте cron:
```bash
# Додайте в crontab (кажді 14 хвилин)
*/14 * * * * curl -s https://prometeylabs-telegram-bot-4mu2.onrender.com/ping > /dev/null
```

## 📱 Тестування бота:

1. **Перезапустіть сервіс на Render**
2. **Дочекайтесь завершення деплою**
3. **Надішліть `/start` боту**
4. **Бот повинен відповісти за 5-10 секунд**

## 🆘 Якщо проблема залишається:

### Перевірте логи:
```bash
# На Render dashboard -> Monitor -> Logs
# Шукайте помилки в логах
```

### Перевірте webhook:
```bash
python3 setup_webhook.py check
```

### Тестуйте endpoint:
```bash
curl https://prometeylabs-telegram-bot-4mu2.onrender.com/
```

## 💡 Альтернативи:

### 1. Upgrade до paid plan на Render:
- Сервіс не буде "спати"
- Миттєві відповіді

### 2. Використовуйте інші хостинги:
- Railway
- Heroku
- DigitalOcean App Platform

### 3. VPS з polling:
- Замініть webhook на polling
- Бот буде сам запитувати оновлення

## 🔍 Діагностичні команди:

```bash
# Перевірка статусу
python3 test_bot_status.py

# Встановлення webhook
python3 setup_webhook.py set

# Перевірка webhook
python3 setup_webhook.py check

# Keep-alive
python3 keep_alive.py
```

## 📞 Підтримка:

Якщо проблема залишається:
1. Перевірте логи на Render
2. Запустіть діагностику
3. Перезапустіть сервіс
4. Встановіть keep-alive
