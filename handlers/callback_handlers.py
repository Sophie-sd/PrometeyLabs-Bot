"""
Обробники callback-запитів для PrometeyLabs Telegram Bot
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import logging
from database import SessionLocal, User, Project, Payment
from google_sheets import get_client_projects, get_client_payments, get_client_statistics
from .menu_utils import (
    get_main_menu_keyboard, get_services_menu_keyboard, get_client_menu_keyboard, get_admin_menu_keyboard,
    get_main_menu_text, get_services_menu_text, get_client_menu_text, get_admin_menu_text
)

logger = logging.getLogger(__name__)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник всіх callback-запитів"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    user = update.effective_user
    
    logger.info(f"Callback від користувача {user.id}: {callback_data}")
    
    try:
        if callback_data.startswith("order_"):
            await handle_order_services(query, context, callback_data)
        elif callback_data.startswith("admin_"):
            await handle_admin_actions(query, context, callback_data)
        elif callback_data in ["my_services", "payments", "statistics", "offers", "documents", "support"]:
            await handle_client_actions(query, context, callback_data)
        elif callback_data in ["about_company"]:
            await handle_info_actions(query, context, callback_data)
        elif callback_data == "services_menu":
            await handle_services_menu(query, context)
        elif callback_data == "back_to_menu":
            await handle_back_to_menu(query, context)
        else:
            await query.edit_message_text("Невідома дія. Спробуйте ще раз.")
            
    except Exception as e:
        logger.error(f"Помилка в callback_handler: {e}")
        await query.edit_message_text("Виникла помилка. Спробуйте ще раз.")

async def handle_order_services(query, context, callback_data):
    """Обробка замовлень послуг"""
    service_info = {
        "order_website": {
            "title": "💻 Замовлення сайту",
            "description": """
🏗️ **Розробка сайту під ключ**

✅ **Що включено:**
• Аналіз цілей та цільової аудиторії
• Унікальний дизайн (без шаблонів!)
• Адаптивна верстка для всіх пристроїв
• SEO-оптимізація
• Інтеграція з CRM та аналітикою
• Навчання керування сайтом

💰 **Ціна:** $100-700
⏱️ **Термін:** до 10 днів

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад до послуг", callback_data="services_menu")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="back_to_menu")]
            ]
        },
        "order_ads": {
            "title": "📢 Запуск реклами",
            "description": """
📢 **Налаштування та оптимізація реклами**

✅ **Платформи:**
• Facebook Ads
• Google Ads
• TikTok

✅ **Що включено:**
• Аналіз цільової аудиторії
• Створення рекламних креативів
• Налаштування таргетингу
• A/B тестування
• Оптимізація за результатами
• Звітність та аналітика

💰 **Ціна:** від $200

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад до послуг", callback_data="services_menu")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="back_to_menu")]
            ]
        },
        "order_video": {
            "title": "🎬 Генерація AI-відео",
            "description": """
🎬 **AI-відео - відео нового покоління**

✅ **Створення роликів на Veo 3 та інших AI-платформах:**
• Будь-які формати: від рекламних до презентаційних
• Сучасна графіка, спецефекти та стиль
• Контент, який привертає увагу

💰 **Ціна:** $1,3 за секунду

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад до послуг", callback_data="services_menu")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="back_to_menu")]
            ]
        },
        "order_social": {
            "title": "📱 Ведення соціальних мереж",
            "description": """
📱 **Комплексне ведення соцмереж**

✅ **Що включено:**
• Стратегія контент-плану
• Створення постів та сторіс
• Дизайн графіки
• Копірайтинг
• Просування та реклама
• Аналітика та звітність

✅ **Платформи:**
• Instagram
• Facebook
• TikTok
• LinkedIn
• YouTube

💰 **Ціна:** від $100/місяць

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад до послуг", callback_data="services_menu")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="back_to_menu")]
            ]
        },
        "order_avatars": {
            "title": "🤖 AI-аватари",
            "description": """
🤖 **AI-аватари - ваш віртуальний образ, що працює за вас**

✅ **Можливості:**
• Виглядають 1:1 як ви або будь-яка людина
• Говорять вашим голосом чи будь-яким іншим
• Можуть відтворити будь-який текст чи сценарій
• Спілкуються на будь-якій мові світу

💰 **Ціна:** від $100 на місяць

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад до послуг", callback_data="services_menu")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="back_to_menu")]
            ]
        },
        "order_bots": {
            "title": "🤖 Telegram-боти",
            "description": """
🤖 **Telegram-боти - автоматизований помічник для бізнесу**

✅ **Що включено:**
• Прийом заявок та замовлень напряму в Telegram
• Інтеграція з оплатами, CRM та аналітикою
• Персональні кабінети, реферальки, нотифікації
• Повна автоматизація від комунікацій до продажів

✅ **Функціональність:**
• Автоматичні відповіді на запитання
• Обробка платежів та замовлень
• Інтеграція з вашим сайтом
• Аналітика та звіти
• Багатомовна підтримка

💰 **Ціна:** $100-700
⏱️ **Термін:** 3-7 днів

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад до послуг", callback_data="services_menu")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="back_to_menu")]
            ]
        },
        "order_education": {
            "title": "🎓 Навчання IT та маркетингу",
            "description": """
🎓 **Курси та майстер-класи**

✅ **Напрямки:**
• Веб-розробка (HTML, CSS, JavaScript, Python)
• UI/UX дизайн
• Цифровий маркетинг
• Штучний інтелект та ML
• SEO та контент-маркетинг

✅ **Формати:**
• Індивідуальні уроки
• Групові курси
• Майстер-класи
• Онлайн навчання

💰 **Ціна:** від $50/урок
⏱️ **Термін:** за індивідуальним планом

🔗 **Зв'яжіться з менеджером:**
• [💬 Telegram](https://t.me/PrometeyLabs)
            """,
            "buttons": [
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]
        }
    }
    
    if callback_data in service_info:
        service = service_info[callback_data]
        reply_markup = InlineKeyboardMarkup(service["buttons"])
        
        await query.edit_message_text(
            f"**{service['title']}**\n\n{service['description']}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_client_actions(query, context, callback_data):
    """Обробка дій клієнтів"""
    user = query.from_user
    
    if callback_data == "my_services":
        # Отримуємо проекти з Google Sheets або бази даних
        projects = get_client_projects(user.id) if hasattr(user, 'id') else []
        
        if projects:
            text = "📊 **Ваші послуги:**\n\n"
            for project in projects:
                text += f"• **{project.get('name', 'Проект')}** - {project.get('status', 'Статус')}\n"
                text += f"  Прогрес: {project.get('progress', 0)}%\n\n"
        else:
            text = "📊 **Ваші послуги:**\n\nУ вас поки немає активних проектів."
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "payments":
        text = "💳 **Оплати та рахунки:**\n\nФункція в розробці. Зверніться до менеджера."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "statistics":
        text = "📈 **Статистика:**\n\nФункція в розробці. Зверніться до менеджера."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "offers":
        text = "🎯 **Пропозиції для вас:**\n\nФункція в розробці. Зверніться до менеджера."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "documents":
        text = "📎 **Ваші документи:**\n\nФункція в розробці. Зверніться до менеджера."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "support":
        text = """
📞 **Підтримка PrometeyLabs**

🔗 **Зв'яжіться з нами:**
• [💬 Telegram](https://t.me/PrometeyLabs) - консультації, менеджер компанії
• [✈️ Telegram-канал](t.me/prometeylabs_channel)
• [📸 Instagram](@prometeylabs)
• [🌐 Сайт](prometeylabs.com)

⏰ **Відповідаємо швидко!**
        """
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_admin_actions(query, context, callback_data):
    """Обробка дій адміністраторів"""
    if callback_data == "admin_clients":
        text = "👤 **Список клієнтів:**\n\nФункція в розробці."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "admin_reports":
        text = "📂 **Завантаження звітів:**\n\nФункція в розробці."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "admin_notifications":
        text = "🔔 **Push-сповіщення:**\n\nФункція в розробці."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif callback_data == "admin_subscriptions":
        text = "📜 **Активні підписки:**\n\nФункція в розробці."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_services_menu(query, context):
    """Обробка меню послуг"""
    keyboard = get_services_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = get_services_menu_text()
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_info_actions(query, context, callback_data):
    """Обробка інформаційних дій"""
    if callback_data == "about_company":
        text = """
🏢 **Про PrometeyLabs**

PrometeyLabs — це не просто студія, а власна система розробки, створена на основі досвіду в коді, дизайні, автоматизації та ШІ.

👥 **Команда:**
• Дизайнери
• Розробники
• Маркетологи
• AI-експерти

🧠 **Наші переваги:**
• Не використовуємо шаблони
• Не працюємо на конструкторах
• Кожен сайт — унікальний, створений вручну
• Власна система компонентів та бібліотек
• Власний LLM для автоматизації рутини

⚡ **Результат:**
• Запуск сайтів до 10 днів
• Ціна $300–700
• Офіційна робота через ФОП Дмитренко Софія Дмитрівна

🔗 **Зв'яжіться з нами:**
• [Telegram](https://t.me/PrometeyLabs)
• [Сайт](prometeylabs.com)
        """
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def show_new_client_menu_callback(query, context, user):
    """Показ меню для нових клієнтів (callback версія)"""
    keyboard = get_main_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_main_menu_text(user.first_name if user else 'користувач')
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def show_client_menu_callback(query, context, user):
    """Показ меню для постійних клієнтів (callback версія)"""
    keyboard = get_client_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_client_menu_text(user.first_name)
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def show_admin_menu_callback(query, context, user):
    """Показ меню для адміністраторів (callback версія)"""
    keyboard = get_admin_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_admin_menu_text(user.first_name)
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_back_to_menu(query, context):
    """Обробка повернення в головне меню"""
    user = query.from_user
    
    # Отримуємо користувача з бази
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        
        if db_user:
            if db_user.is_client:
                await show_client_menu_callback(query, context, db_user)
            elif db_user.is_admin:
                await show_admin_menu_callback(query, context, db_user)
            else:
                await show_new_client_menu_callback(query, context, db_user)
        else:
            await show_new_client_menu_callback(query, context, user)
            
    except Exception as e:
        logger.error(f"Помилка в back_to_menu: {e}")
        await query.edit_message_text("Виникла помилка. Спробуйте /start")
    finally:
        db.close()

def setup_callback_handlers(application):
    """Налаштування обробників callback-запитів"""
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    logger.info("Обробники callback-запитів налаштовані")
