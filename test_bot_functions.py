#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки функціональності PrometeyLabs Telegram Bot
"""
import sys
import os

# Додаємо шлях до проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handlers.menu_utils import (
    get_main_menu_keyboard, get_services_menu_keyboard, 
    get_client_menu_keyboard, get_admin_menu_keyboard,
    get_main_menu_text, get_services_menu_text, 
    get_client_menu_text, get_admin_menu_text
)

def test_menu_keyboards():
    """Тестування клавіатур меню"""
    print("🧪 Тестування клавіатур меню")
    print("=" * 50)
    
    # Тест головного меню
    print("\n🔍 Головне меню:")
    main_menu = get_main_menu_keyboard()
    for i, row in enumerate(main_menu):
        for button in row:
            print(f"  {i+1}. {button.text} -> {button.callback_data}")
    
    # Тест меню послуг
    print("\n🔍 Меню послуг:")
    services_menu = get_services_menu_keyboard()
    for i, row in enumerate(services_menu):
        for button in row:
            print(f"  {i+1}. {button.text} -> {button.callback_data}")
    
    # Тест меню клієнта
    print("\n🔍 Меню клієнта:")
    client_menu = get_client_menu_keyboard()
    for i, row in enumerate(client_menu):
        for button in row:
            print(f"  {i+1}. {button.text} -> {button.callback_data}")
    
    # Тест меню адміна
    print("\n🔍 Меню адміна:")
    admin_menu = get_admin_menu_keyboard()
    for i, row in enumerate(admin_menu):
        for button in row:
            print(f"  {i+1}. {button.text} -> {button.callback_data}")

def test_menu_texts():
    """Тестування текстів меню"""
    print("\n🧪 Тестування текстів меню")
    print("=" * 50)
    
    # Тест головного меню
    print("\n🔍 Текст головного меню:")
    main_text = get_main_menu_text("Тестовий користувач")
    print(main_text[:200] + "..." if len(main_text) > 200 else main_text)
    
    # Тест меню послуг
    print("\n🔍 Текст меню послуг:")
    services_text = get_services_menu_text()
    print(services_text[:200] + "..." if len(services_text) > 200 else services_text)
    
    # Тест меню клієнта
    print("\n🔍 Текст меню клієнта:")
    client_text = get_client_menu_text("Тестовий клієнт")
    print(client_text[:200] + "..." if len(client_text) > 200 else client_text)
    
    # Тест меню адміна
    print("\n🔍 Текст меню адміна:")
    admin_text = get_admin_menu_text("Тестовий адмін")
    print(admin_text[:200] + "..." if len(admin_text) > 200 else admin_text)

def test_callback_data_consistency():
    """Тестування консистентності callback_data"""
    print("\n🧪 Тестування консистентності callback_data")
    print("=" * 50)
    
    # Отримуємо всі клавіатури
    main_menu = get_main_menu_keyboard()
    services_menu = get_services_menu_keyboard()
    client_menu = get_client_menu_keyboard()
    admin_menu = get_admin_menu_keyboard()
    
    # Збираємо всі callback_data
    all_callback_data = set()
    
    for menu in [main_menu, services_menu, client_menu, admin_menu]:
        for row in menu:
            for button in row:
                all_callback_data.add(button.callback_data)
    
    print(f"📊 Всього унікальних callback_data: {len(all_callback_data)}")
    print("\n🔍 Список всіх callback_data:")
    for callback_data in sorted(all_callback_data):
        print(f"  • {callback_data}")
    
    # Перевіряємо наявність всіх необхідних callback_data
    required_callbacks = {
        "services_menu", "back_to_menu", "about_company",
        "order_website", "order_ads", "order_video", "order_social", 
        "order_avatars", "order_bots", "order_education",
        "my_services", "payments", "statistics", "offers", "documents", "support",
        "admin_clients", "admin_reports", "admin_notifications", "admin_subscriptions"
    }
    
    missing_callbacks = required_callbacks - all_callback_data
    if missing_callbacks:
        print(f"\n❌ Відсутні callback_data: {missing_callbacks}")
    else:
        print(f"\n✅ Всі необхідні callback_data присутні")
    
    extra_callbacks = all_callback_data - required_callbacks
    if extra_callbacks:
        print(f"\n⚠️ Додаткові callback_data: {extra_callbacks}")

def main():
    """Головна функція тестування"""
    print("🚀 Тестування функціональності PrometeyLabs Telegram Bot")
    print("=" * 60)
    
    try:
        # Тестуємо клавіатури
        test_menu_keyboards()
        
        # Тестуємо тексти
        test_menu_texts()
        
        # Тестуємо консистентність
        test_callback_data_consistency()
        
        print("\n🎉 Всі тести завершено успішно!")
        
    except Exception as e:
        print(f"\n❌ Помилка при тестуванні: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
