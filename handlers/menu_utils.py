"""
Спільні утиліти для меню PrometeyLabs Telegram Bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    """Отримання клавіатури головного меню"""
    return [
        [InlineKeyboardButton("🛍️ Послуги", callback_data="services_menu")],
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
        [InlineKeyboardButton("🎓 Навчання IT та маркетингу", callback_data="order_education")],
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

🛍️ **Послуги** - Розробка сайтів, реклама, AI-відео, соцмережі, боти, аватари, навчання

ℹ️ **Про компанію** - Інформація про PrometeyLabs та нашу команду

💡 **Наші переваги:**
• Унікальні рішення без шаблонів
• Швидка реалізація (5-10 днів)
• Доступні ціни ($100-700)
• Технічна підтримка

Оберіть потрібний розділ!
    """

def get_services_menu_text():
    """Отримання тексту меню послуг"""
    return """
🛍️ **Наші послуги**

💻 **Замовити сайт** - Розробка сайтів під ключ, унікальний дизайн, SEO-оптимізація
💰 Ціна: $100-700 | ⏱️ Термін: до 10 днів

📢 **Запустити рекламу** - Facebook Ads, Google Ads, TikTok з оптимізацією
💰 Ціна: від $200 | ⏱️ Термін: залежить від кампанії

🎬 **Генерація AI-відео** - Ролики на Veo 3 та інших AI-платформах
💰 Ціна: $1,3/сек | ⏱️ Термін: 1-3 дні

📱 **Ведення соціальних мереж** - Instagram, Facebook, TikTok, LinkedIn, YouTube
💰 Ціна: від $100/міс | ⏱️ Термін: постійно

🤖 **AI-аватари** - Віртуальний образ, що працює за вас
💰 Ціна: від $100/міс | ⏱️ Термін: 3-5 днів

🤖 **Telegram-боти** - Автоматизація бізнесу, CRM, оплати
💰 Ціна: $100-700 | ⏱️ Термін: 3-7 днів

🎓 **Навчання IT та маркетингу** - Курси, майстер-класи, індивідуальні уроки
💰 Ціна: від $50/урок | ⏱️ Термін: за планом

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
• Доступ до документів та договорів
• Технічна підтримка та консультації

💎 **VIP-клієнт:**
• Пріоритетна підтримка
• Знижки на наступні проекти
• Ексклюзивні пропозиції
• Персональний менеджер

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
• Моніторити статистику та аналітику
• Керувати налаштуваннями бота

📊 **Швидка статистика:**
• Загальна кількість клієнтів
• Активні проекти
• Доходи за період
• Популярні послуги

Що потрібно зробити?
    """

# Спільні функції для показу меню (використовуються як в командах, так і в callback)
def show_menu_for_user(user, update_or_query, is_callback=False):
    """Універсальна функція для показу меню користувача"""
    try:
        # Спрощена логіка без залежності від БД
        # За замовчуванням показуємо меню для нових клієнтів
        return show_new_client_menu(update_or_query, user, is_callback)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Помилка показу меню: {e}")
        # Fallback до головного меню
        return show_main_menu(update_or_query, user, is_callback)

def show_new_client_menu(update_or_query, user, is_callback=False):
    """Показ меню для нових клієнтів"""
    keyboard = get_main_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_main_menu_text(user.first_name if user else 'користувач')
    
    if is_callback:
        return update_or_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        return update_or_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

def show_client_menu(update_or_query, user, is_callback=False):
    """Показ меню для постійних клієнтів"""
    keyboard = get_client_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_client_menu_text(user.first_name)
    
    if is_callback:
        return update_or_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        return update_or_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

def show_admin_menu(update_or_query, user, is_callback=False):
    """Показ меню для адміністраторів"""
    keyboard = get_admin_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_admin_menu_text(user.first_name)
    
    if is_callback:
        return update_or_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        return update_or_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

def show_main_menu(update_or_query, user, is_callback=False):
    """Fallback функція для показу головного меню"""
    keyboard = get_main_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_main_menu_text(user.first_name if user else 'користувач')
    
    if is_callback:
        return update_or_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        return update_or_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
