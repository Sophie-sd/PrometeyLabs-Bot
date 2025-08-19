"""
Спільні утиліти для меню PrometeyLabs Telegram Bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    """Отримання клавіатури головного меню"""
    return [
        [InlineKeyboardButton("🛍️ Послуги", callback_data="services_menu")],
        [InlineKeyboardButton("🎓 Навчання", callback_data="order_education")],
        [InlineKeyboardButton("ℹ️ Про компанію", callback_data="about_company")]
    ]

def get_services_menu_keyboard():
    """Отримання клавіатури меню послуг"""
    return [
        [InlineKeyboardButton("💻 Замовити сайт", callback_data="order_website")],
        [InlineKeyboardButton("📢 Запустити рекламу", callback_data="order_ads")],
        [InlineKeyboardButton("🎬 Генерація AI-відео", callback_data="order_video")],
        [InlineKeyboardButton("📱 Ведення соціальних мереж", callback_data="order_social")],
        [InlineKeyboardButton("🤖 AI-аватари", callback_data="order_avatars")],
        [InlineKeyboardButton("🤖 Telegram-боти", callback_data="order_bots")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ]

def get_client_menu_keyboard():
    """Отримання клавіатури меню для постійних клієнтів"""
    return [
        [InlineKeyboardButton("📊 Мої послуги", callback_data="my_services")],
        [InlineKeyboardButton("💳 Оплати та рахунки", callback_data="payments")],
        [InlineKeyboardButton("📈 Статистика", callback_data="statistics")],
        [InlineKeyboardButton("🎯 Пропозиції для мене", callback_data="offers")],
        [InlineKeyboardButton("📎 Мої документи", callback_data="documents")],
        [InlineKeyboardButton("📞 Підтримка", callback_data="support")]
    ]

def get_admin_menu_keyboard():
    """Отримання клавіатури меню для адміністраторів"""
    return [
        [InlineKeyboardButton("👤 Список клієнтів", callback_data="admin_clients")],
        [InlineKeyboardButton("📂 Завантажити звіт", callback_data="admin_reports")],
        [InlineKeyboardButton("🔔 Push-сповіщення", callback_data="admin_notifications")],
        [InlineKeyboardButton("📜 Активні підписки", callback_data="admin_subscriptions")]
    ]

def get_main_menu_text(user_name):
    """Отримання тексту головного меню"""
    return f"""
🎉 Вітаю, {user_name}!

Я офіційний бот PrometeyLabs. Оберіть що вас цікавить:

🛍️ **Послуги** - Перегляд всіх наших послуг

🎓 **Навчання** - Курси та майстер-класи з IT, маркетингу та AI

ℹ️ **Про компанію** - Інформація про PrometeyLabs

Оберіть потрібний розділ!
    """

def get_services_menu_text():
    """Отримання тексту меню послуг"""
    return """
🛍️ **Наші послуги**

💻 **Замовити сайт** - Розробка сайтів будь-якої складності під ключ, готових до SEO-просування, у бюджеті до $700

📢 **Запустити рекламу** - Налаштування та оптимізація Facebook Ads, Google Ads, TikTok

🎬 **Генерація AI-відео** - Створення роликів на Veo 3 та інших AI-платформах

📱 **Ведення соціальних мереж** - Комплексне ведення соцмереж

🤖 **AI-аватари** - Ваш віртуальний образ, що працює за вас

🤖 **Telegram-боти** - Автоматизований помічник для бізнесу

Оберіть потрібну послугу:
    """

def get_client_menu_text(user_name):
    """Отримання тексту меню для постійних клієнтів"""
    return f"""
👋 Вітаю, {user_name}!

Ласкаво просимо в особистий кабінет PrometeyLabs!

Тут ви можете:
• Переглядати свої проекти та їх статус
• Керувати оплатами та рахунками
• Отримувати статистику по роботі
• Бачити спеціальні пропозиції
• Доступ до документів

Що вас цікавить?
    """

def get_admin_menu_text(user_name):
    """Отримання тексту меню для адміністраторів"""
    return f"""
🔐 Вітаю, {user_name}!

Панель адміністратора PrometeyLabs Bot

Тут ви можете:
• Керувати клієнтами та проектами
• Завантажувати звіти з Google Sheets
• Відправляти сповіщення клієнтам
• Переглядати активні підписки

Що потрібно зробити?
    """
