#!/usr/bin/env python3
"""
Скрипт для встановлення webhook для PrometeyLabs Telegram Bot
"""
import requests
import sys
from config import BOT_TOKEN

def set_webhook():
    """Встановлення webhook для бота"""
    
    # URL вашого сервісу на Render
    service_url = "https://prometeylabs-telegram-bot-4mu2.onrender.com"
    webhook_url = f"{service_url}/webhook"
    
    print(f"🔗 Встановлюю webhook: {webhook_url}")
    
    try:
        # Встановлюємо webhook через Telegram API
        telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        data = {
            "url": webhook_url,
            "allowed_updates": ["message", "callback_query", "inline_query"],
            "drop_pending_updates": True
        }
        
        response = requests.post(telegram_api_url, json=data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook встановлено успішно!")
            print(f"📱 Бот готовий до роботи")
            
            # Перевіряємо інформацію про бота
            bot_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
            bot_response = requests.get(bot_info_url)
            bot_info = bot_response.json()
            
            if bot_info.get("ok"):
                bot = bot_info["result"]
                print(f"🤖 Бот: @{bot['username']} ({bot['first_name']})")
            
            # Перевіряємо поточний webhook
            webhook_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
            webhook_response = requests.get(webhook_info_url)
            webhook_info = webhook_response.json()
            
            if webhook_info.get("ok"):
                info = webhook_info["result"]
                print(f"🔗 Webhook URL: {info.get('url', 'Не встановлено')}")
                print(f"📊 Pending updates: {info.get('pending_update_count', 0)}")
                
        else:
            print(f"❌ Помилка встановлення webhook: {result.get('description', 'Невідома помилка')}")
            return False
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False
    
    return True

def delete_webhook():
    """Видалення webhook"""
    print("🗑️ Видаляю webhook...")
    
    try:
        telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.delete(telegram_api_url)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook видалено успішно!")
        else:
            print(f"❌ Помилка видалення: {result.get('description', 'Невідома помилка')}")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")

def check_webhook():
    """Перевірка поточного webhook"""
    print("🔍 Перевіряю поточний webhook...")
    
    try:
        webhook_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
        response = requests.get(webhook_info_url)
        result = response.json()
        
        if result.get("ok"):
            info = result["result"]
            print(f"🔗 Webhook URL: {info.get('url', 'Не встановлено')}")
            print(f"📊 Pending updates: {info.get('pending_update_count', 0)}")
            print(f"🔄 Last error: {info.get('last_error_message', 'Немає помилок')}")
            print(f"⏰ Last error time: {info.get('last_error_date', 'Немає')}")
        else:
            print(f"❌ Помилка отримання інформації: {result.get('description', 'Невідома помилка')}")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "set":
            set_webhook()
        elif command == "delete":
            delete_webhook()
        elif command == "check":
            check_webhook()
        else:
            print("Використання: python setup_webhook.py [set|delete|check]")
    else:
        print("🔧 PrometeyLabs Telegram Bot - Webhook Setup")
        print("Використання:")
        print("  python setup_webhook.py set    - Встановити webhook")
        print("  python setup_webhook.py delete - Видалити webhook")
        print("  python setup_webhook.py check  - Перевірити webhook")
        print()
        
        # Автоматично встановлюємо webhook
        set_webhook()
