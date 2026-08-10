import html

class Tariffs:
    def __init__(self):
        self.tariff_list = []

    def add_tariff(self, type_name: str, places: str, price: str):
        self.tariff_list.append({
            "type": type_name,
            "places": places,
            "price": price
        })

    def __repr__(self):
        return f"Tariffs({self.tariff_list})"

    def to_html(self) -> str:
        if not self.tariff_list:
            return "Билетов нет"

        # Исправлено: t['type'] -> t["type"] (для единообразия)
        type_width = max(len("Тип"), *(len(t["type"]) for t in self.tariff_list))
        places_width = max(len("Мест: 0"), *(len(f"мест: {t['places']}") for t in self.tariff_list))
        price_width = max(len("Цена: 0"), *(len(f"цена: {t['price']}") for t in self.tariff_list))

        lines = []
        for t in self.tariff_list:
            # Исправлено: t.type -> t["type"] (доступ по ключу, а не по атрибуту)
            row = f"{t['type']:<{type_width}} | {'мест: ' + str(t['places']):<{places_width}} | {'цена: ' + str(t['price']):<{price_width}}"
            lines.append(f"<code>{html.escape(row)}</code>")

        return "\n".join(lines)