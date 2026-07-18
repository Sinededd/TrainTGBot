import json

from src.models.train import Train


def save_train(train, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(train.__dict__, f, ensure_ascii=False, indent=2)

def load_train(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return Train(
            data["train_number"], data["date"], data["route"],
            data["dep_time"], data["dep_station"], data["arr_time"],
            data["arr_station"], data["duration"], data["id"], data["tariffs"]
        )