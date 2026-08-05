from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    surname: str
    name: str
    patronymic: str
    passport_number: str
    login: str
    password: str
    created_at: Optional[str] = None