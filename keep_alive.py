#!/usr/bin/env python3
"""
Keep-alive скрипт для PrometeyLabs Telegram Bot на Render
Підтримує сервіс активним на free tier
"""
import requests
import time
import schedule
import logging
from datetime import datetime

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# URL вашого сервісу
SERVICE_URL = "https://prometeylabs-telegram-bot-4mu2.onrender.com"

def ping_service():
    """Відправляє ping до сервісу"""
    try:
        logger.info("🔄 Відправляю ping до сервісу...")
        
        # Пробуємо health check
        health_response = requests.get(f"{SERVICE_URL}/", timeout=30)
        if health_response.status_code == 200:
            health_data = health_response.json()
            logger.info(f"✅ Health check: {health_data.get('status')} | Bot: {health_data.get('bot_status')}")
        else:
            logger.warning(f"⚠️  Health check failed: HTTP {health_response.status_code}")
        
        # Пробуємо ping endpoint
        ping_response = requests.get(f"{SERVICE_URL}/ping", timeout=30)
        if ping_response.status_code == 200:
            ping_data = ping_response.json()
            logger.info(f"✅ Ping: {ping_data.get('pong')} | {ping_data.get('timestamp')}")
        else:
            logger.warning(f"⚠️  Ping failed: HTTP {ping_response.status_code}")
            
        return True
        
    except requests.exceptions.Timeout:
        logger.warning("⏰ Таймаут - сервіс може бути в режимі сну")
        return False
    except requests.exceptions.ConnectionError:
        logger.error("❌ Помилка з'єднання - сервіс недоступний")
        return False
    except Exception as e:
        logger.error(f"❌ Помилка ping: {e}")
        return False

def test_webhook():
    """Тестує webhook endpoint"""
    try:
        logger.info("🔗 Тестую webhook endpoint...")
        
        webhook_response = requests.get(f"{SERVICE_URL}/bot_info", timeout=30)
        if webhook_response.status_code == 200:
            bot_data = webhook_response.json()
            if bot_data.get('status') == 'success':
                logger.info("✅ Webhook endpoint працює")
                return True
            else:
                logger.warning(f"⚠️  Webhook endpoint має проблеми: {bot_data.get('error')}")
                return False
        else:
            logger.warning(f"⚠️  Webhook endpoint недоступний: HTTP {webhook_response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Помилка тесту webhook: {e}")
        return False

def main():
    """Головна функція"""
    logger.info("🚀 Keep-alive скрипт запущено")
    logger.info(f"🎯 Сервіс: {SERVICE_URL}")
    
    # Перший ping
    ping_service()
    
    # Плануємо ping кожні 14 хвилин (Render free tier засинає через 15 хв неактивності)
    schedule.every(14).minutes.do(ping_service)
    
    # Плануємо тест webhook кожні 30 хвилин
    schedule.every(30).minutes.do(test_webhook)
    
    logger.info("📅 Планування:")
    logger.info("   - Ping кожні 14 хвилин")
    logger.info("   - Webhook тест кожні 30 хвилин")
    logger.info("   - Натисніть Ctrl+C для зупинки")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Перевіряємо кожну хвилину
            
    except KeyboardInterrupt:
        logger.info("🛑 Keep-alive скрипт зупинено користувачем")
    except Exception as e:
        logger.error(f"❌ Критична помилка: {e}")

if __name__ == "__main__":
    main()
