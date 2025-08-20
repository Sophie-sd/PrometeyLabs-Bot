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
        logger.error(f"Помилка при створенні бота: {e}")
        return False

@app.route('/')
def health_check():
    """Перевірка здоров'я сервісу для Render"""
    return jsonify({
        "status": "healthy",
        "service": "PrometeyLabs Telegram Bot",
        "version": "1.0.0"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обробка веб-хуків від Telegram"""
    if bot_application is None:
        return jsonify({"error": "Bot not initialized"}), 500
    
    try:
        # Отримуємо дані від Telegram
        update_data = request.get_json()
        
        # Створюємо Update об'єкт та обробляємо його
        from telegram import Update
        update = Update.de_json(update_data, bot_application.bot)
        
        # Обробляємо оновлення
        bot_application.process_update(update)
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logger.error(f"Помилка в webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Встановлення веб-хука для Telegram"""
    if bot_application is None:
        return jsonify({"error": "Bot not initialized"}), 500
    
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
    if bot_application is None:
        return jsonify({"error": "Bot not initialized"}), 500
    
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
    if bot_application is None:
        return jsonify({"error": "Bot not initialized"}), 500
    
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
    if create_bot():
        # Запускаємо Flask сервер
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        logger.error("Не вдалося створити бота. Завершення роботи.")
        exit(1)
