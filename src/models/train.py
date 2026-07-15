class Train:
    def __init__(self, train_number, date_, route, dep_time, dep_station, arr_time, arr_station, duration, train_id, tariffs):
        self.train_number = train_number
        self.date = date_
        self.route = route
        self.dep_time = dep_time
        self.dep_station = dep_station
        self.arr_time = arr_time
        self.arr_station = arr_station
        self.duration = duration
        self.id = train_id
        self.tariffs = tariffs

    def __repr__(self):
        return f"Train({self.train_number}: {self.route} | {self.dep_time} -> {self.arr_time})"