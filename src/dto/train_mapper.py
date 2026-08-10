from dto.train_entity import TrainEntity
from models.train import Train
from utils.convert_date_time import get_datetime_iso


class TrainMapper:
    @staticmethod
    def to_train_entity(train: Train) -> TrainEntity:
        return TrainEntity(
            train_id=train.id,
            train_number=train.train_number,
            from_station=train.from_station,
            to_station=train.to_station,
            departure_datetime=get_datetime_iso(train.date, train.from_time)
        )