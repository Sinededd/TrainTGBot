import os
from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

ENV_FILE = DATA_DIR / ".env"


def init_environment():
    """Checks for .env and requests/generates missing keys."""
    load_dotenv(ENV_FILE)

    if not os.getenv("SECRET_ENCRYPTION_KEY"):
        new_key = Fernet.generate_key().decode()
        set_key(ENV_FILE, "SECRET_ENCRYPTION_KEY", new_key)
        print("🔑 Generated and saved a new SECRET_ENCRYPTION_KEY")

    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("\n--- Initial setup ---")
        token = input("🤖 Enter the Telegram bot API token: ").strip()
        while not token:
            token = input("Token cannot be empty. Enter the API token: ").strip()

        set_key(ENV_FILE, "TELEGRAM_BOT_TOKEN", token)
        print("✅ Token saved to .env\n")

    load_dotenv(ENV_FILE, override=True)