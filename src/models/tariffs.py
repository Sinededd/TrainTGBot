class Tariffs:
    def __init__(self):
        self.tariffs_list = []

    def add_tariff(self, type_name: str, places: str, price: str):
        self.tariffs_list.append({
            "type": type_name,
            "places": places,
            "price": price
        })

    def __repr__(self):
        return f"Tariffs({self.tariffs_list})"