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
    get_main_menu_text, get_client_menu_text, get_admin_menu_text,
    show_menu_for_user, show_new_client_menu, show_client_menu, show_admin_menu
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
        await show_menu_for_user(db_user, update, is_callback=False)
            
    except Exception as e:
        logger.error(f"Помилка в start_command: {e}")
        await update.message.reply_text("Виникла помилка. Спробуйте ще раз.")
    finally:
        db.close()

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
    
    await update.message.reply_text(support_text, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Користувач {update.effective_user.id} звернувся до підтримки")

def setup_command_handlers(application):
    """Налаштування обробників команд"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("support", support_command))
    
    logger.info("Обробники команд налаштовані")
