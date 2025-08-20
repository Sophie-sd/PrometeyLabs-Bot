#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки веб-хуків PrometeyLabs Telegram Bot
"""
import requests
import json
import sys

def test_health_check(base_url):
    """Тест перевірки здоров'я сервісу"""
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_bot_info(base_url):
    """Тест отримання інформації про бота"""
    try:
        response = requests.get(f"{base_url}/bot_info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bot info: {data}")
            return True
        else:
            print(f"❌ Bot info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bot info error: {e}")
        return False

def test_set_webhook(base_url):
    """Тест встановлення веб-хука"""
    try:
        webhook_url = f"{base_url}/webhook"
        response = requests.get(f"{base_url}/set_webhook", params={"url": base_url})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook set: {data}")
            return True
        else:
            print(f"❌ Webhook set failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Webhook set error: {e}")
        return False

def test_delete_webhook(base_url):
    """Тест видалення веб-хука"""
    try:
        response = requests.get(f"{base_url}/delete_webhook")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook deleted: {data}")
            return True
        else:
            print(f"❌ Webhook delete failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Webhook delete error: {e}")
        return False

def main():
    """Головна функція тестування"""
    if len(sys.argv) != 2:
        print("Використання: python test_webhook.py <base_url>")
        print("Приклад: python test_webhook.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    print(f"🧪 Тестування сервісу: {base_url}")
    print("=" * 50)
    
    # Тестуємо всі ендпоінти
    tests = [
        ("Health Check", lambda: test_health_check(base_url)),
        ("Bot Info", lambda: test_bot_info(base_url)),
        ("Set Webhook", lambda: test_set_webhook(base_url)),
        ("Delete Webhook", lambda: test_delete_webhook(base_url)),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Тестування: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Помилка тесту: {e}")
            results.append((test_name, False))
    
    # Підсумок
    print("\n" + "=" * 50)
    print("📊 Результати тестування:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Загальний результат: {passed}/{total} тестів пройдено")
    
    if passed == total:
        print("🎉 Всі тести пройдено успішно!")
        sys.exit(0)
    else:
        print("⚠️ Деякі тести не пройдено")
        sys.exit(1)

if __name__ == "__main__":
    main()
