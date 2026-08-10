from dateutil import parser


class TrainEntity:
    def __init__(self, train_id : str, train_number : str,  from_station : str, to_station : str, departure_datetime : str):
        self.id = train_id
        self.train_number = train_number
        self.from_station = from_station
        self.to_station = to_station
        self.departure_datetime = departure_datetime

    def get_date(self):
        dt = parser.parse(self.departure_datetime)
        return dt.date()

    def get_time(self):
        dt = parser.parse(self.departure_datetime)
        return dt.strftime("%H:%M")

    def __repr__(self):
        return f"Train({self.id}: {self.departure_datetime} | {self.from_station} -> {self.to_station})"
