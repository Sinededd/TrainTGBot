import json
from dataclasses import dataclass
from typing import Optional, Callable, Any


@dataclass
class Seat:
    number: int
    carNumber: int
    hasTable: bool
    typeAbbr: str
    price: float

class AvailableSeats:

    def __init__(self):
        self.seats = []

    def add(self, number: int, carNumber, hasTable: bool, typeAbbr: str, price: float) -> None:
        self.seats.append(Seat(number, carNumber, hasTable, typeAbbr, price))

    def clear(self) -> None:
        self.seats = []

    def get_first(
            self,
            filter_func: Optional[Callable[[Seat], bool]] = None,
            sort_key: Optional[Callable[[Seat], Any]] = None,
            reverse: bool = False
    ) -> Optional[Seat]:
        """Returns the first seat after filtering and sorting"""

        filtered_seats = self.seats
        if filter_func:
            filtered_seats = [seat for seat in filtered_seats if filter_func(seat)]

        if not filtered_seats:
            return None

        if sort_key:
            filtered_seats = sorted(filtered_seats, key=sort_key, reverse=reverse)

        return filtered_seats[0]

    def __repr__(self) -> str:
        return json.dumps(self.seats, indent=2, ensure_ascii=False, default=str)
