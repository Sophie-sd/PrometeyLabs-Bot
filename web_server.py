"""
Веб-сервер для PrometeyLabs Telegram Bot на Render
Підтримка python-telegram-bot v21 + Telegram Business
"""
from flask import Flask, request, jsonify
import os
import logging
import asyncio
from telegram.ext import Application
from telegram import Update, BotCommand
from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION
from handlers import setup_command_handlers, setup_message_handlers, setup_callback_handlers
from utils.logger import setup_logging

# Налаштування логування
logger = setup_logging()

# Створення Flask додатку
app = Flask(__name__)

# Глобальна змінна для бота
bot_application = None

async def error_handler(update, context):
    """Обробник помилок"""
    try:
        if update and update.effective_user:
            user_id = update.effective_user.id
            username = update.effective_user.username or "Unknown"
            logger.error(f"Помилка при обробці оновлення від користувача {user_id} (@{username}): {context.error}")
        else:
            logger.error(f"Помилка при обробці оновлення: {context.error}")
    except Exception as e:
        logger.error(f"Помилка в error_handler: {e}")

def run_async(coro):
    """Запуск асинхронної функції в синхронному контексті"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

def create_bot():
    """Створення та налаштування бота"""
    global bot_application
    
    try:
        # Перевіряємо базу даних
        try:
            from database import init_database
            if not init_database():
                logger.error("Не вдалося ініціалізувати базу даних")
                return False
            logger.info("✅ База даних готова")
        except Exception as e:
            logger.error(f"Помилка ініціалізації БД: {e}")
            return False
        
        # Створення застосунку з підтримкою Business
        bot_application = Application.builder().token(BOT_TOKEN).build()
        
        # Налаштування обробників
        setup_command_handlers(bot_application)
        setup_message_handlers(bot_application)
        setup_callback_handlers(bot_application)
        
        # Додаємо обробник помилок
        bot_application.add_error_handler(error_handler)
        
        # ІНІЦІАЛІЗУЄМО Application (обов'язково для v21!)
        run_async(bot_application.initialize())
        
        # Налаштовуємо команди бота
        run_async(setup_bot_commands())
        
        # Налаштовуємо кнопку меню
        run_async(setup_chat_menu_button())
        
        logger.info(f"✅ Бот {BOT_NAME} створений та ініціалізовано успішно!")
        return True
        
    except Exception as e:
        logger.error(f"Помилка при створенні бота: {e}", exc_info=True)
        return False

async def setup_bot_commands():
    """Налаштування команд бота"""
    try:
        commands = [
            BotCommand("start", "Почати роботу з ботом"),
            BotCommand("menu", "Показати головне меню"),
            BotCommand("help", "Допомога по боту"),
            BotCommand("support", "Зв'язатися з підтримкою")
        ]
        
        await bot_application.bot.set_my_commands(commands)
        logger.info("✅ Команди бота налаштовано")
        
    except Exception as e:
        logger.error(f"Помилка налаштування команд: {e}")

async def setup_chat_menu_button():
    """Налаштування кнопки меню чату"""
    try:
        from telegram import MenuButtonCommands
        
        await bot_application.bot.set_chat_menu_button(
            menu_button=MenuButtonCommands()
        )
        logger.info("✅ Кнопка меню чату налаштовано")
        
    except Exception as e:
        logger.error(f"Помилка налаштування кнопки меню: {e}")

def log_update_details(update):
    """Логування деталей оновлення для діагностики Business"""
    try:
        update_id = update.update_id
        has_business_connection = bool(update.business_connection)
        
        # Правильно беремо business_connection_id з effective_message
        if update.effective_message:
            from_id = update.effective_message.from_user.id if update.effective_message.from_user else "N/A"
            chat_id = update.effective_message.chat.id if update.effective_message.chat else "N/A"
            business_connection_id = getattr(update.effective_message, 'business_connection_id', None)
            
            logger.info(f"📱 Update {update_id}: bcid={business_connection_id}, from={from_id}, chat={chat_id}, "
                       f"business_connection={has_business_connection}")
        elif update.callback_query:
            # Для callback запитів
            from_id = update.callback_query.from_user.id if update.callback_query.from_user else "N/A"
            chat_id = update.callback_query.message.chat.id if update.callback_query.message else "N/A"
            business_connection_id = getattr(update.callback_query.message, 'business_connection_id', None)
            
            logger.info(f"📱 Update {update_id}: bcid={business_connection_id}, from={from_id}, chat={chat_id}, "
                       f"callback_query")
        else:
            logger.info(f"📱 Update {update_id}: business_connection={has_business_connection}")
            
    except Exception as e:
        logger.error(f"Помилка логування деталей update: {e}")

def stop_bot():
    """Зупинка бота"""
    global bot_application
    
    if bot_application:
        try:
            run_async(bot_application.stop())
            run_async(bot_application.shutdown())
            logger.info("✅ Бот зупинено успішно")
        except Exception as e:
            logger.error(f"Помилка при зупинці бота: {e}")
        finally:
            bot_application = None

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
    
    # Перевіряємо чи бот дійсно ініціалізований
    try:
        if hasattr(bot_application, '_initialized') and bot_application._initialized:
            return True
        else:
            logger.warning("Бот створено, але не ініціалізовано. Переініціалізую...")
            run_async(bot_application.initialize())
            return True
    except Exception as e:
        logger.error(f"Помилка перевірки ініціалізації: {e}")
        return False

@app.route('/')
def health_check():
    """Перевірка здоров'я сервісу для Render"""
    try:
        # Простий health check без складних операцій
        bot_status = "initialized" if bot_application else "not_initialized"
        
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
        
        # Додаємо додаткову інформацію про бота (тільки якщо він готовий)
        if bot_application and bot_application.bot and bot_status == "initialized":
            try:
                # Викликаємо get_me АСИНХРОННО
                bot_info = run_async(bot_application.bot.get_me())
                health_info["bot_details"] = {
                    "id": bot_info.id,
                    "username": bot_info.username,
                    "first_name": bot_info.first_name
                }
            except Exception as e:
                health_info["bot_details"] = {"error": str(e)}
        
        return jsonify(health_info)
        
    except Exception as e:
        logger.error(f"Помилка в health check: {e}")
        # Повертаємо простий response навіть при помилці
        return jsonify({
            "status": "error",
            "service": "PrometeyLabs Telegram Bot",
            "error": str(e),
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }), 500

@app.route('/ping')
def ping():
    """Keep-alive endpoint для Render free tier"""
    try:
        # Простий ping без складних операцій
        bot_status = "initialized" if bot_application else "not_initialized"
        
        ping_info = {
            "pong": True,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "bot_status": bot_status,
            "message": "Keep-alive ping successful"
        }
        
        return jsonify(ping_info)
        
    except Exception as e:
        logger.error(f"Помилка в ping: {e}")
        # Повертаємо простий response навіть при помилці
        return jsonify({
            "pong": False,
            "error": str(e),
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }), 500

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
        update = Update.de_json(update_data, bot_application.bot)
        
        # Логуємо деталі для діагностики Business
        log_update_details(update)
        
        # Обробляємо оновлення АСИНХРОННО
        try:
            run_async(bot_application.process_update(update))
            logger.info(f"Webhook оброблено успішно: {update.update_id}")
            return jsonify({"status": "ok", "update_id": update.update_id})
        except Exception as process_error:
            logger.error(f"Помилка обробки оновлення: {process_error}")
            return jsonify({"error": "Update processing failed"}), 500
        
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
        
        # Встановлюємо веб-хук АСИНХРОННО
        success = run_async(bot_application.bot.set_webhook(url=webhook_url))
        
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
        success = run_async(bot_application.bot.delete_webhook())
        
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
        # Викликаємо get_me АСИНХРОННО
        bot_info = run_async(bot_application.bot.get_me())
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
    
    # Додаємо обробник сигналів для правильної зупинки
    import signal
    import sys
    
    def signal_handler(sig, frame):
        logger.info("Отримано сигнал зупинки, зупиняю бота...")
        stop_bot()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Спробуємо створити бота, але не зупиняємо сервер при помилці
    try:
        if create_bot():
            logger.info("Бот створено успішно!")
        else:
            logger.warning("Бот не створено при запуску, але сервер продовжує роботу")
    except Exception as e:
        logger.error(f"Помилка при створенні бота: {e}")
        logger.warning("Сервер продовжує роботу, бот буде створено при першому запиті")
    
    # Запускаємо Flask сервер в будь-якому випадку
    logger.info("Запускаю Flask сервер...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
