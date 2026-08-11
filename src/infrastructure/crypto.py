import os
from functools import lru_cache

from cryptography.fernet import Fernet
from dotenv import load_dotenv


@lru_cache
def _get_cipher() -> Fernet:
    load_dotenv()
    key = os.getenv("SECRET_ENCRYPTION_KEY")
    if not key:
        raise ValueError("SECRET_ENCRYPTION_KEY not found in environment!")
    return Fernet(key.encode())


def encrypt_text(text: str) -> str:
    if not text:
        return ""
    return _get_cipher().encrypt(text.encode()).decode()


def decrypt_text(encrypted_text: str) -> str:
    if not encrypted_text:
        return ""
    return _get_cipher().decrypt(encrypted_text.encode()).decode()
