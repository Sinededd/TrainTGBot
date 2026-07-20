import json
from dataclasses import dataclass
from typing import Optional, Callable, Any


@dataclass
class Seat:
    number: str
    carNumber: str
    hasTable: bool
    typeAbbr: str
    price: float

class AvailableSeats:

    def __init__(self):
        self.seats = []

    def add(self, number: str, carNumber: str, hasTable: bool, typeAbbr: str, price: float) -> None:
        self.seats.append(Seat(number, carNumber, hasTable, typeAbbr, price))

    def clear(self) -> None:
        self.seats = []


    def get_all(
            self,
            filter_func: Optional[Callable[[Seat], bool]] = None,
            sort_key: Optional[Callable[[Seat], Any]] = None,
            reverse: bool = False
    ) -> list[Seat]:
        """Returns seats after filtering and sorting"""

        filtered_seats = self.seats
        if filter_func:
            filtered_seats = [seat for seat in filtered_seats if filter_func(seat)]

        if sort_key:
            filtered_seats = sorted(filtered_seats, key=sort_key, reverse=reverse)

        return filtered_seats


    def get_first(
            self,
            filter_func: Optional[Callable[[Seat], bool]] = None,
            sort_key: Optional[Callable[[Seat], Any]] = None,
            reverse: bool = False
    ) -> Optional[Seat]:
        """Returns the first seat after filtering and sorting or None if not found"""
        result = self.get_all(filter_func, sort_key, reverse)
        return result[0] if result else None


    def __repr__(self) -> str:
        return json.dumps(self.seats, indent=2, ensure_ascii=False, default=str)
