"""
Обробники callback-запитів для PrometeyLabs Telegram Bot
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import logging
from .menu_utils import (
    get_main_menu_keyboard, get_services_menu_keyboard, get_client_menu_keyboard, get_admin_menu_keyboard,
    get_main_menu_text, get_services_menu_text, get_client_menu_text, get_admin_menu_text,
    show_menu_for_user, show_new_client_menu, show_client_menu, show_admin_menu
)

logger = logging.getLogger(__name__)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник всіх callback-запитів"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    user = update.effective_user
    
    # Визначаємо business_connection_id для callback
    business_connection_id = getattr(query.message, 'business_connection_id', None)
    
    logger.info(f"Callback від користувача {user.id}: {callback_data} з bcid={business_connection_id}")
    
    try:
        if callback_data.startswith("order_"):
            logger.info(f"Обробка замовлення послуги: {callback_data}")
            await handle_order_services(query, context, callback_data)
        elif callback_data.startswith("admin_"):
            logger.info(f"Обробка адмін дії: {callback_data}")
            await handle_admin_actions(query, context, callback_data)
        elif callback_data in ["my_services", "payments", "statistics", "offers", "documents", "support"]:
            logger.info(f"Обробка клієнтської дії: {callback_data}")
            await handle_client_actions(query, context, callback_data)
        elif callback_data in ["about_company"]:
            logger.info(f"Обробка інформаційної дії: {callback_data}")
            await handle_info_actions(query, context, callback_data)
        elif callback_data == "services_menu":
            logger.info("Показ меню послуг")
            await handle_services_menu(query, context)
        elif callback_data == "back_to_menu":
            logger.info("Повернення в головне меню")
            await handle_back_to_menu(query, context)
        else:
            logger.warning(f"Невідома callback дія: {callback_data}")
            # Визначаємо business_connection_id для відповіді
            business_connection_id = getattr(query.message, 'business_connection_id', None)
            await query.edit_message_text(
                "Невідома дія. Спробуйте ще раз.",
                business_connection_id=business_connection_id
            )
            
    except Exception as e:
        logger.error(f"Помилка в callback_handler: {e}")
        # Визначаємо business_connection_id для відповіді
        business_connection_id = getattr(query.message, 'business_connection_id', None)
        await query.edit_message_text(
            "Виникла помилка. Спробуйте ще раз.",
            business_connection_id=business_connection_id
        )

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
• SEO-оптимізація та налаштування
• Інтеграція з CRM та аналітикою
• Навчання керування сайтом
• Технічна підтримка 1 місяць

✅ **Типи сайтів:**
• Лендінги та односторінкові сайти
• Корпоративні сайти
• Інтернет-магазини
• Сайти послуг та портфоліо
• Веб-додатки

💰 **Ціна:** $100-700
⏱️ **Термін:** 5-10 днів

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

✅ **Створення роликів на AI-платформах:**
• Veo 3, Runway, Pika Labs, Sora
• Будь-які формати: від рекламних до презентаційних
• Сучасна графіка, спецефекти та стиль
• Контент, який привертає увагу та конвертує

✅ **Типи відео:**
• Рекламні ролики
• Презентаційні відео
• Соціальні мережі (TikTok, Instagram, YouTube)
• Корпоративні відео
• Обучальні матеріали

💰 **Ціна:** $1,3 за секунду готового відео
⏱️ **Термін:** 1-3 дні

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
• Працюють 24/7 без перерв

✅ **Застосування:**
• Відео-презентації
• Обучальні матеріали
• Рекламні ролики
• Клієнтська підтримка
• Персональні повідомлення

💰 **Ціна:** від $100 на місяць
⏱️ **Термін створення:** 3-5 днів

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
• Технічна підтримка 1 місяць

✅ **Функціональність:**
• Автоматичні відповіді на запитання
• Обробка платежів та замовлень
• Інтеграція з вашим сайтом
• Аналітика та звіти
• Багатомовна підтримка
• Адмін-панель для керування

✅ **Типи ботів:**
• Боти для замовлень
• Боти підтримки
• Боти для навчання
• Боти для розваг
• Боти для бізнесу

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
• Веб-розробка (HTML, CSS, JavaScript, Python, React, Node.js)
• UI/UX дизайн (Figma, Adobe XD, Sketch)
• Цифровий маркетинг (Google Ads, Facebook Ads, SEO)
• Штучний інтелект та ML (Python, TensorFlow, PyTorch)
• SEO та контент-маркетинг
• Графічний дизайн (Photoshop, Illustrator, Canva)

✅ **Формати:**
• Індивідуальні уроки (1-на-1)
• Групові курси (до 10 осіб)
• Майстер-класи (2-4 години)
• Онлайн навчання (Zoom, Google Meet)
• Гібридне навчання

✅ **Рівні:**
• Початківці (0 досвіду)
• Середній рівень
• Просунутий рівень
• Експертний рівень

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
        
        logger.info(f"Показ послуги: {service['title']}")
        
        await query.edit_message_text(
            f"**{service['title']}**\n\n{service['description']}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        logger.warning(f"Послуга не знайдена: {callback_data}")
        await query.edit_message_text("Послуга не знайдена. Спробуйте ще раз.")

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
• [✈️ Telegram-канал](t.me/prometeylabs_channel) - новини та оновлення
• [📸 Instagram](@prometeylabs) - наші роботи та кейси
• [🌐 Сайт](prometeylabs.com) - детальна інформація

⏰ **Відповідаємо швидко!**
• Робочі години: Пн-Пт 9:00-18:00 (Київ)
• Екстрені питання: 24/7 через Telegram
• Середній час відповіді: 15-30 хвилин

💡 **Часті питання:**
• Як замовити послугу?
• Які документи потрібні?
• Як проходить оплата?
• Чи надаєте гарантію?

**Напишіть ваше питання, і ми відповімо найближчим часом!**
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
• Дизайнери (UI/UX, графічні)
• Розробники (Frontend, Backend, Mobile)
• Маркетологи (Digital, SEO, SMM)
• AI-експерти (ML, генеративні моделі)

🧠 **Наші переваги:**
• Не використовуємо шаблони
• Не працюємо на конструкторах
• Кожен сайт — унікальний, створений вручну
• Власна система компонентів та бібліотек
• Власний LLM для автоматизації рутини
• Індивідуальний підхід до кожного клієнта

⚡ **Результат:**
• Запуск сайтів за 5-10 днів
• Ціна $100–700 (залежить від складності)
• Офіційна робота через ФОП Дмитренко Софія Дмитрівна
• Технічна підтримка та навчання

🔗 **Зв'яжіться з нами:**
• [Telegram](https://t.me/PrometeyLabs)
• [Сайт](prometeylabs.com)
        """
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# Функції показу меню тепер винесені в menu_utils.py для уникнення дублювання

async def handle_back_to_menu(query, context):
    """Обробка повернення в головне меню"""
    user = query.from_user
    
    try:
        # Показуємо головне меню без залежності від БД
        await show_new_client_menu(query, user, is_callback=True)
            
    except Exception as e:
        logger.error(f"Помилка в back_to_menu: {e}")
        await query.edit_message_text("Виникла помилка. Спробуйте /start")

def setup_callback_handlers(application):
    """Налаштування обробників callback-запитів"""
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    logger.info("Обробники callback-запитів налаштовані")
