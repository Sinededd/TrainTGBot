from dataclasses import dataclass


@dataclass
class Subscription:
    def __init__(self, user_id: int, train_id: str):
        self.user_id: int = user_id
        self.train_id: str = train_id