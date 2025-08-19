"""
Обробники команд для PrometeyLabs Telegram Bot
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
import logging
from database import SessionLocal, User, Project, Payment
from google_sheets import get_client_projects, get_client_payments, get_client_statistics
from .menu_utils import (
    get_main_menu_keyboard, get_client_menu_keyboard, get_admin_menu_keyboard,
    get_main_menu_text, get_client_menu_text, get_admin_menu_text
)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start"""
    user = update.effective_user
    
    # Перевіряємо чи користувач вже є в базі
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        
        if not db_user:
            # Створюємо нового користувача
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            db.add(db_user)
            db.commit()
            logger.info(f"Створено нового користувача: {user.id}")
        
        # Показуємо головне меню
        if db_user.is_client:
            await show_client_menu(update, context, db_user)
        elif db_user.is_admin:
            await show_admin_menu(update, context, db_user)
        else:
            await show_new_client_menu(update, context, db_user)
            
    except Exception as e:
        logger.error(f"Помилка в start_command: {e}")
        await update.message.reply_text("Виникла помилка. Спробуйте ще раз.")
    finally:
        db.close()

async def show_new_client_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Показ меню для нових клієнтів"""
    keyboard = get_main_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_main_menu_text(user.first_name)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def show_client_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Показ меню для постійних клієнтів"""
    keyboard = get_client_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_client_menu_text(user.first_name)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def show_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Показ меню для адміністраторів"""
    keyboard = get_admin_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = get_admin_menu_text(user.first_name)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

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

📞 **Підтримка:**
• Telegram: https://t.me/PrometeyLabs
• Email: info@prometeylabs.com
• Сайт: prometeylabs.com

Якщо у вас є питання, просто напишіть мені повідомлення!
    """
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Користувач {update.effective_user.id} запросив допомогу")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /menu"""
    await start_command(update, context)

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /support"""
    support_text = """
📞 **Підтримка PrometeyLabs**

🔗 **Зв'яжіться з нами:**
• [✈️ Telegram-канал](t.me/prometeylabs_channel)
• [Telegram](https://t.me/PrometeyLabs) - консультації, менеджер компанії
• [📸 Instagram](@prometeylabs)
• [🌐 Сайт](prometeylabs.com)

⏰ **Відповідаємо швидко!**

💬 **Або просто напишіть ваше питання, і ми відповімо найближчим часом.**
    """
    
    await update.message.reply_text(support_text, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Користувач {update.effective_user.id} звернувся до підтримки")

def setup_command_handlers(application):
    """Налаштування обробників команд"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("support", support_command))
    
    logger.info("Обробники команд налаштовані")
