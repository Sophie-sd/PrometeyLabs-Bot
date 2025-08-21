"""
Обробники команд для PrometeyLabs Telegram Bot
"""
from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
import logging
from .menu_utils import show_menu_for_user, get_main_menu_keyboard, get_main_menu_text

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start"""
    user = update.effective_user
    
    try:
        # Показуємо головне меню з ReplyKeyboard для Business
        await show_main_menu_with_reply_keyboard(update, user)
        logger.info(f"Користувач {user.id} запустив бота")
            
    except Exception as e:
        logger.error(f"Помилка в start_command: {e}")
        # Fallback - просте меню без залежності від утиліт
        from .menu_utils import get_main_menu_text, get_main_menu_keyboard
        await update.message.reply_text(
            get_main_menu_text(user.first_name or "Користувач"),
            reply_markup=InlineKeyboardMarkup(get_main_menu_keyboard())
        )

# Функції показу меню тепер винесені в menu_utils.py для уникнення дублювання

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /help"""
    help_text = """
🔧 Допомога по боту PrometeyLabs

📱 **Основні команди:**
• /start - Почати роботу з ботом
• /help - Показати цю довідку
• /menu - Показати головне меню
• /support - Зв'язатися з підтримкою

💡 **Як користуватися:**
1. Натисніть /start для початку роботи
2. Оберіть потрібну послугу з меню
3. Слідуйте інструкціям бота
4. Для замовлення зв'яжіться з менеджером

🛍️ **Доступні послуги:**
• 💻 Розробка сайтів ($100-700)
• 📢 Реклама (від $200)
• 🎬 AI-відео ($1,3/сек)
• 📱 Соцмережі (від $100/міс)
• 🤖 AI-аватари (від $100/міс)
• 🤖 Telegram-боти ($100-700)
• 🎓 Навчання IT та маркетингу (від $50/урок)

📞 **Підтримка:**
• Telegram: https://t.me/PrometeyLabs
• Email: info@prometeylabs.com
• Сайт: prometeylabs.com

💬 **Або просто напишіть ваше питання, і ми відповімо найближчим часом!**
    """
    
    # Визначаємо business_connection_id
    business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
    
    await update.message.reply_text(
        help_text, 
        parse_mode=ParseMode.MARKDOWN,
        business_connection_id=business_connection_id
    )
    logger.info(f"Користувач {update.effective_user.id} запросив допомогу з bcid={business_connection_id}")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /menu"""
    user = update.effective_user
    
    try:
        # Показуємо головне меню з ReplyKeyboard
        await show_main_menu_with_reply_keyboard(update, user)
        logger.info(f"Користувач {user.id} запросив меню")
            
    except Exception as e:
        logger.error(f"Помилка в menu_command: {e}")
        # Fallback - просте меню
        await update.message.reply_text(
            get_main_menu_text(user.first_name or "Користувач"),
            reply_markup=InlineKeyboardMarkup(get_main_menu_keyboard())
        )

async def show_main_menu_with_reply_keyboard(update: Update, user):
    """Показ головного меню з ReplyKeyboard для Business"""
    try:
        # Створюємо ReplyKeyboard
        keyboard = [
            [KeyboardButton("🛍️ Послуги"), KeyboardButton("ℹ️ Про компанію")],
            [KeyboardButton("📞 Підтримка"), KeyboardButton("💼 Мій кабінет")]
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, 
            one_time_keyboard=False, 
            resize_keyboard=True
        )
        
        # Визначаємо чи це Business чат (правильно з effective_message)
        business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
        
        # Логуємо для діагностики
        logger.info(f"Відправляю ReplyKeyboard меню з bcid={business_connection_id}")
        
        # Відправляємо меню
        await update.message.reply_text(
            get_main_menu_text(user.first_name or "Користувач"),
            reply_markup=reply_markup,
            business_connection_id=business_connection_id
        )
        
    except Exception as e:
        logger.error(f"Помилка показу ReplyKeyboard меню: {e}")
        # Fallback до InlineKeyboard
        await update.message.reply_text(
            get_main_menu_text(user.first_name or "Користувач"),
            reply_markup=InlineKeyboardMarkup(get_main_menu_keyboard())
        )

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /support"""
    support_text = """
📞 **Підтримка PrometeyLabs**

🔗 **Зв'яжіться з нами:**
• [✈️ Telegram-канал](t.me/prometeylabs_channel) - новини та оновлення
• [Telegram](https://t.me/PrometeyLabs) - консультації, менеджер компанії
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

💬 **Або просто напишіть ваше питання, і ми відповімо найближчим часом!**
    """
    
    # Визначаємо business_connection_id
    business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
    
    await update.message.reply_text(
        support_text, 
        parse_mode=ParseMode.MARKDOWN,
        business_connection_id=business_connection_id
    )
    logger.info(f"Користувач {update.effective_user.id} звернувся до підтримки з bcid={business_connection_id}")

def setup_command_handlers(application):
    """Налаштування обробників команд"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("support", support_command))
    
    logger.info("Обробники команд налаштовані")
