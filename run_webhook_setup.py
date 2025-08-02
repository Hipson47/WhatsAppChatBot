#!/usr/bin/env python3
"""
Jednorazowy skrypt do ustawienia webhooka dla Telegram bota.

Ten skrypt konfiguruje webhook URL dla bota, dzięki czemu Telegram będzie
wysyłał wiadomości bezpośrednio na serwer zamiast używać polling.
"""

import os
import sys
import asyncio
import logging
from telegram import Bot
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

# Dodaj src do ścieżki Python dla importów
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def setup_webhook():
    """
    Asynchroniczna funkcja do ustawienia webhooka dla Telegram bota.
    """
    # Wczytaj token z zmiennej środowiskowej
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not telegram_bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN nie jest ustawiony w zmiennych środowiskowych!")
        print("❌ BŁĄD: Nie znaleziono TELEGRAM_BOT_TOKEN w zmiennych środowiskowych.")
        print("💡 Upewnij się, że ustawiłeś zmienną TELEGRAM_BOT_TOKEN przed uruchomieniem skryptu.")
        return False
    
    # Stały URL webhooka
    webhook_url = "https://chatbot-service-157843431191.europe-west1.run.app"
    
    try:
        # Inicjalizuj bota
        bot = Bot(token=telegram_bot_token)
        
        print(f"🤖 Łączenie z Telegram Bot API...")
        logger.info(f"Inicjalizacja bota i próba ustawienia webhooka: {webhook_url}")
        
        # Sprawdź aktualny webhook
        current_webhook = await bot.get_webhook_info()
        logger.info(f"Aktualny webhook: {current_webhook.url}")
        
        if current_webhook.url == webhook_url:
            print(f"✅ Webhook jest już ustawiony na: {webhook_url}")
            print("ℹ️  Nie ma potrzeby zmiany konfiguracji.")
            return True
        
        # Ustaw nowy webhook
        print(f"🔄 Ustawianie webhooka na: {webhook_url}")
        success = await bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True,  # Usuń pending wiadomości z polling
            max_connections=40,  # Optymalizacja dla Cloud Run
            allowed_updates=["message", "callback_query"]  # Tylko potrzebne typy aktualizacji
        )
        
        if success:
            print(f"✅ SUKCES! Webhook został pomyślnie ustawiony.")
            print(f"🌐 URL webhooka: {webhook_url}")
            print(f"📱 Twój bot będzie teraz otrzymywał wiadomości przez webhook zamiast polling.")
            logger.info("Webhook został pomyślnie skonfigurowany")
            
            # Weryfikacja
            verification = await bot.get_webhook_info()
            print(f"✅ Weryfikacja: webhook aktywny na {verification.url}")
            return True
        else:
            print(f"❌ BŁĄD: Nie udało się ustawić webhooka.")
            logger.error("Telegram API zwrócił False dla set_webhook")
            return False
            
    except Exception as e:
        print(f"❌ BŁĄD podczas ustawiania webhooka: {e}")
        logger.error(f"Wyjątek podczas ustawiania webhooka: {e}", exc_info=True)
        return False


async def remove_webhook():
    """
    Funkcja pomocnicza do usunięcia webhooka (przywrócenie polling).
    """
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not telegram_bot_token:
        print("❌ TELEGRAM_BOT_TOKEN nie jest ustawiony!")
        return False
    
    try:
        bot = Bot(token=telegram_bot_token)
        print("🔄 Usuwanie webhooka...")
        
        success = await bot.delete_webhook(drop_pending_updates=True)
        
        if success:
            print("✅ Webhook został usunięty. Bot wróci do trybu polling.")
            return True
        else:
            print("❌ Nie udało się usunąć webhooka.")
            return False
            
    except Exception as e:
        print(f"❌ BŁĄD podczas usuwania webhooka: {e}")
        return False


def main():
    """
    Główna funkcja skryptu.
    """
    print("=" * 60)
    print("🚀 TELEGRAM WEBHOOK SETUP")
    print("=" * 60)
    print()
    
    # Sprawdź argument wiersza poleceń
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        print("🗑️  Tryb usuwania webhooka...")
        success = asyncio.run(remove_webhook())
    else:
        print("⚙️  Tryb ustawiania webhooka...")
        success = asyncio.run(setup_webhook())
    
    print()
    print("=" * 60)
    if success:
        print("🎉 OPERACJA ZAKOŃCZONA POMYŚLNIE!")
    else:
        print("💥 OPERACJA NIEUDANA!")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()