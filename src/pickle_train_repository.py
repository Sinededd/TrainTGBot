import pickle

from train_repository import TrainRepository


class PickleTrainRepository(TrainRepository):
    """Реализация TrainRepository с использованием Pickle для сериализации"""

    def __init__(self, filename: str):
        self.filename = filename

    def get_by_id(self, train_id: str):
        try:
            with open(self.filename, 'rb') as f:
                trains = pickle.load(f)
                return trains.get(train_id)
        except FileNotFoundError:
            return None

    def save(self, train):
        try:
            with open(self.filename, 'rb') as f:
                trains = pickle.load(f)
        except FileNotFoundError:
            trains = {}

        trains[train.id] = train
        with open(self.filename, 'wb') as f:
            pickle.dump(trains, f)