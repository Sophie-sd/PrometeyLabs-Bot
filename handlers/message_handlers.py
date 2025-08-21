"""
Обробники повідомлень для PrometeyLabs Telegram Bot
"""
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, MessageHandler, filters
import logging

logger = logging.getLogger(__name__)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник текстових повідомлень"""
    user = update.effective_user
    message_text = update.message.text.lower()
    
    logger.info(f"Отримано повідомлення від {user.id}: {message_text}")
    
    # Визначаємо чи це Business чат (правильно з effective_message)
    business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
    
    # Простий аналіз повідомлення
    if any(word in message_text for word in ['привіт', 'вітаю', 'hello', 'hi']):
        response = f"Привіт, {user.first_name}! 👋 Радий вас бачити!"
    elif any(word in message_text for word in ['як справи', 'як дела', 'how are you']):
        response = "Дякую, у мене все добре! 😊 А у вас як справи?"
    elif any(word in message_text for word in ['допомога', 'help', 'підтримка']):
        response = "Звичайно! Напишіть /help для отримання списку доступних команд."
    elif any(word in message_text for word in ['ціни', 'прайс', 'prices', 'cost']):
        response = "Для отримання інформації про ціни наших послуг, будь ласка, зверніться до нас:\n📧 info@prometeylabs.com"
    elif any(word in message_text for word in ['проект', 'project', 'розробка', 'development']):
        response = "💻 Ми спеціалізуємося на розробці веб та мобільних додатків! Напишіть /start для детальної інформації."
    elif any(word in message_text for word in ['сайт', 'website', 'веб-сайт']):
        response = "💻 Ми створюємо унікальні сайти під ключ за $300-700! Напишіть /start для замовлення."
    elif any(word in message_text for word in ['реклама', 'ads', 'маркетинг']):
        response = "📢 Налаштовуємо рекламу на Facebook, Google, TikTok! Напишіть /start для деталей."
    elif any(word in message_text for word in ['відео', 'video', 'ai']):
        response = "🎬 Створюємо AI-відео з озвученням! Напишіть /start для замовлення."
    elif any(word in message_text for word in ['соцмережі', 'instagram', 'facebook']):
        response = "📱 Ведемо соціальні мережі комплексно! Напишіть /start для деталей."
    elif any(word in message_text for word in ['навчання', 'курси', 'уроки']):
        response = "🎓 Проводимо курси з IT, маркетингу та AI! Напишіть /start для інформації."
    else:
        # Якщо це перше повідомлення від користувача - показуємо меню
        response = f"Вітаю, {user.first_name}! 👋\n\nЛаскаво просимо до PrometeyLabs! Оберіть що вас цікавить:"
        
        # Створюємо ReplyKeyboard для Business
        keyboard = [
            [KeyboardButton("🛍️ Послуги"), KeyboardButton("ℹ️ Про компанію")],
            [KeyboardButton("📞 Підтримка"), KeyboardButton("💼 Мій кабінет")]
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, 
            one_time_keyboard=False, 
            resize_keyboard=True
        )
        
        await update.message.reply_text(
            response,
            reply_markup=reply_markup,
            business_connection_id=business_connection_id
        )
        return
    
    # Відправляємо відповідь з підтримкою Business
    await update.message.reply_text(
        response,
        business_connection_id=business_connection_id
    )
    logger.info(f"Відправлено відповідь користувачу {user.id}")

async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник фото повідомлень"""
    user = update.effective_user
    
    response = f"Дякую за фото, {user.first_name}! 📸\n\nНа жаль, я поки що не можу аналізувати зображення. Спробуйте написати текст або використати команди."
    
    # Визначаємо business_connection_id
    business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
    
    await update.message.reply_text(
        response,
        business_connection_id=business_connection_id
    )
    logger.info(f"Отримано фото від користувача {user.id} з bcid={business_connection_id}")

async def handle_document_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник документів"""
    user = update.effective_user
    document = update.message.document
    
    response = f"Дякую за документ '{document.file_name}', {user.first_name}! 📄\n\nНа жаль, я поки що не можу обробляти документи. Спробуйте написати текст або використати команди."
    
    # Визначаємо business_connection_id
    business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
    
    await update.message.reply_text(
        response,
        business_connection_id=business_connection_id
    )
    logger.info(f"Отримано документ від користувача {user.id}: {document.file_name} з bcid={business_connection_id}")

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник голосових повідомлень"""
    user = update.effective_user
    
    response = f"Дякую за голосове повідомлення, {user.first_name}! 🎤\n\nНа жаль, я поки що не можу розпізнавати мову. Спробуйте написати текст або використати команди."
    
    # Визначаємо business_connection_id
    business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
    
    await update.message.reply_text(
        response,
        business_connection_id=business_connection_id
    )
    logger.info(f"Отримано голосове повідомлення від користувача {user.id} з bcid={business_connection_id}")

def setup_message_handlers(application):
    """Налаштування обробників повідомлень"""
    # Обробники різних типів повідомлень
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_message
    ))
    
    application.add_handler(MessageHandler(
        filters.PHOTO,
        handle_photo_message
    ))
    
    application.add_handler(MessageHandler(
        filters.Document.ALL,
        handle_document_message
    ))
    
    application.add_handler(MessageHandler(
        filters.VOICE,
        handle_voice_message
    ))
    
    logger.info("Обробники повідомлень налаштовані")
