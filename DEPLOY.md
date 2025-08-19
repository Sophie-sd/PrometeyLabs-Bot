# 🚀 Інструкції по деплою PrometeyLabs Telegram Bot

## 📋 Перед деплоєм

### 1. Підготовка GitHub репозиторію
```bash
# Додайте remote origin (замініть на ваш URL)
git remote add origin https://github.com/your-username/prometeylabs_telegram_bot.git

# Запушіть код
git push -u origin main
```

### 2. Перевірте наявність всіх файлів:
- ✅ `main.py` - головний файл бота
- ✅ `requirements.txt` - залежності Python
- ✅ `render.yaml` - конфігурація для Render
- ✅ `.env.example` - приклад змінних середовища
- ✅ `.gitignore` - ігнорування конфіденційних файлів

## 🌐 Деплой на Render.com

### Крок 1: Створення акаунту
1. Зайдіть на [render.com](https://render.com)
2. Зареєструйтесь через GitHub

### Крок 2: Створення нового сервісу
1. Натисніть **"New +"**
2. Виберіть **"Web Service"**
3. Підключіть ваш GitHub репозиторій

### Крок 3: Налаштування сервісу
```
Name: prometeylabs-telegram-bot
Environment: Python 3
Region: Frankfurt (EU Central) - найближчий до України
Branch: main
Root Directory: (залиште порожнім)
```

### Крок 4: Build & Deploy налаштування
```
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

### Крок 5: Змінні середовища
Додайте наступні змінні:

| Key | Value | Sync |
|-----|-------|------|
| `BOT_TOKEN` | `your_actual_bot_token` | ❌ False |
| `LOG_LEVEL` | `INFO` | ✅ True |
| `PYTHON_VERSION` | `3.9.16` | ✅ True |

**⚠️ Важливо:** `BOT_TOKEN` має бути **Sync: False** для безпеки!

### Крок 6: Запуск деплою
1. Натисніть **"Create Web Service"**
2. Дочекайтесь завершення build процесу
3. Перевірте логи на наявність помилок

## 🔧 Перевірка роботи

### 1. Логи сервісу
- Перейдіть в розділ **"Logs"**
- Перевірте чи немає помилок
- Має бути повідомлення: "Бот PrometeyLabs Bot запущений успішно!"

### 2. Тестування бота
- Відправте `/start` вашому боту
- Перевірте чи відповідає на команди
- Протестуйте навігацію по меню

### 3. Перевірка змінних середовища
- В розділі **"Environment"** переконайтесь що `BOT_TOKEN` встановлений
- Значення має бути замасковане (****)

## 🚨 Розв'язання проблем

### Помилка: "Module not found"
```bash
# Перевірте requirements.txt
# Додайте відсутні залежності
pip install package_name
pip freeze > requirements.txt
```

### Помилка: "BOT_TOKEN not found"
- Перевірте чи додали змінну `BOT_TOKEN` в Render
- Переконайтесь що `Sync: False` для цієї змінної

### Помилка: "Port already in use"
- Render автоматично призначає порт
- Перевірте `render.yaml` конфігурацію

### Бот не відповідає
- Перевірте логи на помилки
- Переконайтесь що токен правильний
- Перевірте чи не заблокований бот

## 📱 Налаштування Telegram Webhook (опціонально)

Якщо потрібен webhook замість polling:

### 1. Отримайте URL вашого сервісу
```
https://your-service-name.onrender.com
```

### 2. Встановіть webhook
```python
# В main.py замініть run_polling() на:
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
    webhook_url="https://your-service-name.onrender.com"
)
```

### 3. Оновіть render.yaml
```yaml
services:
  - type: web
    name: prometeylabs-telegram-bot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: LOG_LEVEL
        value: INFO
      - key: PYTHON_VERSION
        value: 3.9.16
    # Додайте для webhook:
    healthCheckPath: /
```

## 🔄 Автоматичні оновлення

### GitHub Actions (рекомендовано)
1. Створіть `.github/workflows/deploy.yml`
2. Налаштуйте автоматичний деплой при push в main
3. Render автоматично оновить сервіс

### Ручне оновлення
```bash
# Після змін в коді:
git add .
git commit -m "Update bot functionality"
git push origin main

# Render автоматично перезапустить сервіс
```

## 📊 Моніторинг

### Render Dashboard
- **Uptime**: Перевірте чи сервіс працює
- **Logs**: Моніторте помилки та дії бота
- **Metrics**: CPU, пам'ять, мережева активність

### Telegram Bot API
- Перевірте статистику бота через @BotFather
- Моніторте кількість користувачів та повідомлень

## 🎯 Фінальна перевірка

Перед закриттям деплою переконайтесь що:

- ✅ Бот запускається без помилок
- ✅ Всі команди працюють правильно
- ✅ Меню навігація функціонує
- ✅ Логування працює
- ✅ Змінні середовища налаштовані
- ✅ Сервіс доступний з інтернету

## 🆘 Підтримка

Якщо виникли проблеми:
1. Перевірте логи в Render
2. Перевірте налаштування змінних середовища
3. Переконайтесь що код комітиться в правильну гілку
4. Зверніться до команди PrometeyLabs

**Успішного деплою! 🚀**
