"""
Веб-сервер для PrometeyLabs Telegram Bot на Render
"""
from flask import Flask, request, jsonify
import os
import logging
from telegram.ext import Application
from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION
from handlers import setup_command_handlers, setup_message_handlers, setup_callback_handlers
from utils.logger import setup_logging
from database import create_tables

# Налаштування логування
logger = setup_logging()

# Створення Flask додатку
app = Flask(__name__)

# Глобальна змінна для бота
bot_application = None

def create_bot():
    """Створення та налаштування бота"""
    global bot_application
    
    try:
        # Створення таблиць бази даних
        create_tables()
        logger.info("База даних створена/підключена успішно")
        
        # Створення застосунку
        bot_application = Application.builder().token(BOT_TOKEN).build()
        
        # Налаштування обробників
        setup_command_handlers(bot_application)
        setup_message_handlers(bot_application)
        setup_callback_handlers(bot_application)
        
        logger.info(f"Бот {BOT_NAME} створений успішно!")
        return True
        
    except Exception as e:
        logger.error(f"Помилка при створенні бота: {e}", exc_info=True)
        return False

def ensure_bot_initialized():
    """Перевірка та ініціалізація бота якщо потрібно"""
    global bot_application
    
    if bot_application is None:
        logger.warning("Бот не ініціалізований, спробую створити...")
        
        # Спробуємо створити бота кілька разів
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Спроба ініціалізації бота {attempt + 1}/{max_retries}")
                if create_bot():
                    logger.info("Бот успішно ініціалізовано")
                    return True
                else:
                    logger.warning(f"Спроба {attempt + 1} невдала")
            except Exception as e:
                logger.error(f"Помилка при спробі {attempt + 1}: {e}")
            
            if attempt < max_retries - 1:
                import time
                time.sleep(2)  # Чекаємо 2 секунди перед наступною спробою
        
        logger.error("Всі спроби ініціалізації бота невдалі")
        return False
    
    return True

@app.route('/')
def health_check():
    """Перевірка здоров'я сервісу для Render"""
    # Автоматично ініціалізуємо бота якщо потрібно
    if not bot_application:
        logger.info("Health check: спробую автоматично ініціалізувати бота...")
        ensure_bot_initialized()
    
    bot_status = "initialized" if bot_application else "not_initialized"
    
    # Детальна інформація про стан
    health_info = {
        "status": "healthy",
        "service": "PrometeyLabs Telegram Bot",
        "version": "1.0.0",
        "bot_status": bot_status,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "endpoints": {
            "health": "/",
            "ping": "/ping",
            "webhook": "/webhook",
            "bot_info": "/bot_info",
            "set_webhook": "/set_webhook"
        }
    }
    
    # Додаємо додаткову інформацію про бота
    if bot_application and bot_application.bot:
        try:
            bot_info = bot_application.bot.get_me()
            health_info["bot_details"] = {
                "id": bot_info.id,
                "username": bot_info.username,
                "first_name": bot_info.first_name
            }
        except Exception as e:
            health_info["bot_details"] = {"error": str(e)}
    
    return jsonify(health_info)

@app.route('/ping')
def ping():
    """Keep-alive endpoint для Render free tier"""
    # Автоматично ініціалізуємо бота якщо потрібно
    bot_status = "initialized" if bot_application else "not_initialized"
    
    ping_info = {
        "pong": True,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "bot_status": bot_status,
        "message": "Keep-alive ping successful"
    }
    
    # Якщо бот не ініціалізований, спробуємо його створити
    if not bot_application:
        if ensure_bot_initialized():
            ping_info["bot_status"] = "initialized"
            ping_info["message"] = "Bot auto-initialized during ping"
    
    return jsonify(ping_info)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обробка веб-хуків від Telegram"""
    # Автоматично ініціалізуємо бота якщо потрібно
    if not ensure_bot_initialized():
        logger.error("Не вдалося ініціалізувати бота для webhook")
        return jsonify({"error": "Bot initialization failed"}), 500
    
    try:
        # Отримуємо дані від Telegram
        update_data = request.get_json()
        
        if not update_data:
            logger.warning("Webhook отримано порожні дані")
            return jsonify({"error": "Empty data"}), 400
        
        logger.info(f"Webhook отримано: {update_data.get('update_id', 'unknown')}")
        
        # Створюємо Update об'єкт та обробляємо його
        from telegram import Update
        update = Update.de_json(update_data, bot_application.bot)
        
        # Обробляємо оновлення
        bot_application.process_update(update)
        
        logger.info(f"Webhook оброблено успішно: {update.update_id}")
        return jsonify({"status": "ok", "update_id": update.update_id})
        
    except Exception as e:
        logger.error(f"Помилка в webhook: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Встановлення веб-хука для Telegram"""
    if not ensure_bot_initialized():
        return jsonify({"error": "Bot initialization failed"}), 500
    
    try:
        # Отримуємо URL сервісу
        service_url = request.args.get('url')
        if not service_url:
            return jsonify({"error": "URL parameter required"}), 400
        
        webhook_url = f"{service_url}/webhook"
        
        # Встановлюємо веб-хук
        success = bot_application.bot.set_webhook(url=webhook_url)
        
        if success:
            logger.info(f"Webhook встановлено: {webhook_url}")
            return jsonify({
                "status": "success",
                "webhook_url": webhook_url
            })
        else:
            return jsonify({"error": "Failed to set webhook"}), 500
            
    except Exception as e:
        logger.error(f"Помилка при встановленні webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Видалення веб-хука"""
    if not ensure_bot_initialized():
        return jsonify({"error": "Bot initialization failed"}), 500
    
    try:
        success = bot_application.bot.delete_webhook()
        
        if success:
            logger.info("Webhook видалено")
            return jsonify({"status": "success", "message": "Webhook deleted"})
        else:
            return jsonify({"error": "Failed to delete webhook"}), 500
            
    except Exception as e:
        logger.error(f"Помилка при видаленні webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot_info', methods=['GET'])
def bot_info():
    """Інформація про бота"""
    if not ensure_bot_initialized():
        return jsonify({"error": "Bot initialization failed"}), 500
    
    try:
        bot_info = bot_application.bot.get_me()
        return jsonify({
            "status": "success",
            "bot_info": {
                "id": bot_info.id,
                "username": bot_info.username,
                "first_name": bot_info.first_name,
                "can_join_groups": bot_info.can_join_groups,
                "can_read_all_group_messages": bot_info.can_read_all_group_messages,
                "supports_inline_queries": bot_info.supports_inline_queries
            }
        })
        
    except Exception as e:
        logger.error(f"Помилка при отриманні інформації про бота: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Створюємо бота при запуску
    logger.info("Запуск PrometeyLabs Telegram Bot Web Server...")
    
    if create_bot():
        logger.info("Бот створено успішно, запускаю Flask сервер...")
        # Запускаємо Flask сервер
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        logger.error("Не вдалося створити бота. Завершення роботи.")
        exit(1)
