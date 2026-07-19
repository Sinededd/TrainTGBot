from typing import Dict

from models.available_seats import AvailableSeats


def extract_seats(json_data: Dict) -> AvailableSeats:
    """Extract seats from railcar data"""

    av_seats = AvailableSeats()

    for tariff in json_data.get('tariffs', []):
        for car in tariff.get('cars', []):
            for emptyPlaces in car.get('emptyPlaces', []):
                av_seats.add(emptyPlaces, car.get('number'), False, tariff.get('typeAbbr'), float(tariff.get('price_byn').replace(',', '.')))

    print(av_seats)
    return av_seats
