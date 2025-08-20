# 🚀 Швидкий деплой PrometeyLabs Telegram Bot

## ⚡ 5 кроків до успішного деплою

### 1️⃣ Підготуйте репозиторій
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2️⃣ Створіть сервіс на Render
- Зайдіть на [render.com](https://render.com)
- **New +** → **Blueprint**
- Підключіть GitHub репозиторій
- Виберіть гілку `main`

### 3️⃣ Налаштуйте змінні середовища
| Змінна | Значення | Sync |
|--------|----------|------|
| `BOT_TOKEN` | `your_bot_token` | ❌ False |
| `LOG_LEVEL` | `INFO` | ✅ True |

### 4️⃣ Дочекайтесь деплою
- Build: `pip install -r requirements.txt`
- Start: `gunicorn web_server:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
- Статус: **Live** ✅

### 5️⃣ Налаштуйте веб-хук
```bash
# Встановіть веб-хук
https://your-app.onrender.com/set_webhook?url=https://your-app.onrender.com

# Перевірте статус
https://your-app.onrender.com/bot_info
```

## 🔍 Перевірка роботи

### Тестування API
```bash
python test_webhook.py https://your-app.onrender.com
```

### Перевірка в браузері
- `https://your-app.onrender.com/` - Health check
- `https://your-app.onrender.com/bot_info` - Інформація про бота

## 🚨 Якщо щось не працює

1. **Перевірте логи** в Render Dashboard
2. **Переконайтесь** що `BOT_TOKEN` встановлений
3. **Перезапустіть** сервіс
4. **Перевірте** всі файли закомічені

## 📞 Підтримка

- GitHub Issues
- Render Community
- PrometeyLabs Team

**Успішного деплою! 🎉**
