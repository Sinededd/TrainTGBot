import html

from utils.convert_data import convert_to_ddmmyyyy


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


    def to_html(self) -> str:
        date_str = convert_to_ddmmyyyy(self.date)

        t_num = html.escape(str(self.train_number))
        r = html.escape(str(self.route))
        dep_s = html.escape(str(self.dep_station))
        dep_t = html.escape(str(self.dep_time))
        arr_s = html.escape(str(self.arr_station))
        arr_t = html.escape(str(self.arr_time))
        dur = html.escape(str(self.duration))

        return (
            f"<b>Поезд:</b> {t_num}\n"
            f"<b>Дата:</b> {date_str}\n"
            f"<b>Маршрут:</b> {r}\n"
            f"{dep_s} {dep_t} → {arr_s} {arr_t}\n"
            f"<b>В пути:</b> {dur}\n"
            f"<code>────────────────────────────</code>\n"
            f"{self.tariffs.to_html()}"
        )