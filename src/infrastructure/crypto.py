import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("SECRET_ENCRYPTION_KEY")
if not KEY:
    raise ValueError("SECRET_ENCRYPTION_KEY не найден в файле .env!")

cipher = Fernet(KEY.encode())

def encrypt_text(text: str) -> str:
    if not text:
        return ""
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text: str) -> str:
    if not encrypted_text:
        return ""
    return cipher.decrypt(encrypted_text.encode()).decode()