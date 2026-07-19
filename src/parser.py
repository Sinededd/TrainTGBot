import json
import os
import time
import urllib.parse
from datetime import date, datetime
from typing import Dict

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import BrowserContext

from repository.train_repository import TrainRepository
from .models.tariffs import Tariffs
from .models.train import Train
from no_trains_found_exception import NoTrainsFoundException


load_dotenv()


class Parser:
    """Network parser for the Belarusian Railway website."""

    def __init__(self, context: BrowserContext, trainRepository: TrainRepository):
        self.trainRepository = trainRepository
        self.context = context


    async def login(self):
        page = await self.context.new_page()
        await page.goto("https://pass.rw.by/ru/")
        close_button = page.locator(".close").first

        if await close_button.is_visible():
            await close_button.click()
        await page.get_by_role("button", name="Принять").click()
        await page.get_by_role("link", name="Личный кабинет").click()

        login_val = os.getenv("BY_LOGIN")
        password_val = os.getenv("BY_PASSWORD")
        if not login_val or not password_val:
            raise ValueError(
                "Error:  BY_LOGIN or BY_PASSWORD not found in dotenv! "
                "Check your dotenv file and try again."
            )

        await page.get_by_role("textbox", name="Логин/E-mail").fill(login_val)
        await page.get_by_role("textbox", name="Пароль").fill(password_val)
        await page.get_by_role("button", name="Войти").click()

        await page.close()



    async def get_trains(self, station_from: str, station_to: str, date_val: date) -> list[Train]:
        train_list = []

        # Формируем GET-параметры запроса (аналог .data() в Jsoup)
        params = {
            "from": station_from,
            "from_exp": "",
            "from_esr": "",
            "to": station_to,
            "to_exp": "",
            "to_esr": "",
            "front_date": "",
            "date": str(date_val)  # Преобразует дату в формат YYYY-MM-DD
        }
        url = f"https://pass.rw.by/ru/route?{urllib.parse.urlencode(params)}"

        page = await self.context.new_page()
        try:
            await page.goto(url)
            try:
                await page.wait_for_selector("div.sch-table__row-wrap.js-row, .h3, .error_title", timeout=15000)
            except Exception:
                pass
            html_content = await page.content()
        finally:
            await page.close()

        # --- 3. Парсинг страницы с помощью BeautifulSoup ---
        soup = BeautifulSoup(html_content, "html.parser")

        # Ищем все блоки поездов
        trains = soup.select("div.sch-table__row-wrap.js-row")

        # Если поездов нет на странице, проверяем наличие ошибок
        if not trains:
            h3_el = soup.select_one(".h3")
            err_str = h3_el.get_text(strip=True) if h3_el else ""
            if err_str:
                print(f"Ошибка: {err_str}")
                if "Пожалуйста, укажите пункт отправления / прибытия" in err_str:
                    raise NoTrainsFoundException("Неверно указаны пункты отправления / прибытия")

            err_title_el = soup.select_one(".error_title")
            err_title_str = err_title_el.get_text(strip=True) if err_title_el else ""
            if err_title_str:
                print(f"Ошибка: {err_title_str}")
                if "Информация о расписании движения поездов и стоимости проезда на указанную дату недоступна" in err_title_str:
                    raise NoTrainsFoundException(
                        "Информация о расписании движения поездов и стоимости проезда на указанную дату недоступна")

        # Итерируемся по найденным поездам
        for train in trains:
            # Номер поезда
            num_el = train.select_one(".train-number")
            train_number = num_el.get_text(strip=True) if num_el else ""

            # Маршрут
            route_el = train.select_one(".train-route")
            route = route_el.get_text(strip=True) if route_el else ""

            # Время отправления
            dep_time_el = train.select_one(".train-from-time")
            dep_time = dep_time_el.get_text(strip=True) if dep_time_el else ""

            # Станция отправления
            dep_station_el = train.select_one(".train-from-name")
            dep_station = dep_station_el.get_text(strip=True) if dep_station_el else ""

            # Время прибытия
            arr_time_el = train.select_one(".train-to-time")
            arr_time = arr_time_el.get_text(strip=True) if arr_time_el else ""

            # Станция прибытия
            arr_station_el = train.select_one(".train-to-name")
            arr_station = arr_station_el.get_text(strip=True) if arr_station_el else ""

            # Время в пути
            duration_el = train.select_one(".train-duration-time")
            duration = duration_el.get_text(strip=True) if duration_el else ""

            # ID поезда из атрибута data-train-id
            row_el = train.select_one(".sch-table__row")
            train_id = row_el.get("data-train-id", "") if row_el else ""

            # --- Сбор тарифов ---
            tariffs = Tariffs()
            tickets = train.select(".sch-table__t-item")

            for ticket in tickets:
                type_el = ticket.select_one(".sch-table__t-name")
                type_val = ""

                if type_el and type_el.get_text(strip=True):
                    type_val = type_el.get_text(strip=True)
                elif ticket.select_one("i.svg-tag-bicycle--quantity"):
                    type_val = "Вело"

                # Ограничение длины строки до 8 символов (аналог Java-кода)
                type_val = type_val[:8]

                places_el = ticket.select_one(".sch-table__t-quant span")
                places = places_el.get_text(strip=True) if places_el else ""

                price_el = ticket.select_one(".ticket-cost")
                price = price_el.get_text(strip=True) if price_el else ""

                tariffs.add_tariff(type_val, places, price)

            # Создаем объект поезда (вместо паттерна Builder в Python лаконичнее использовать именованные аргументы)
            train_obj = Train(
                train_number=train_number,
                date_=date_val,
                route=route,
                dep_time=dep_time,
                dep_station=dep_station,
                arr_time=arr_time,
                arr_station=arr_station,
                duration=duration,
                train_id=train_id,
                tariffs=tariffs
            )
            train_list.append(train_obj)

        # --- 4. Сохранение отладочных файлов (как в вашем исходном коде) ---
        # try:
        #     with open("page.html", "w", encoding="utf-8") as f:
        #         f.write(soup.prettify())
        #
        #     with open("trains.html", "w", encoding="utf-8") as f:
        #         # Объединяем HTML всех найденных строк в один файл
        #         f.write("\n".join(str(t) for t in trains))
        # except Exception as e:
        #     print(f"Не удалось сохранить отладочные файлы: {e}")
        await page.close()
        return train_list


    async def get_train_data(self, train_id: str) -> Dict:
        train = self.trainRepository.get_by_id(train_id)

        # Create and send request
        dt = datetime.strptime(
            f"{train.date} {train.dep_time}",
            "%Y-%m-%d %H:%M"
        )
        params = {
            "from": train.dep_station,
            "to": train.arr_station,
            "date": train.date,
            "train_number": train.train_number,
            "car_type": "2",                    # !!! Пользователь должен иметь возможно устанавливать приоритет  типов вагона или отключать ненужные
            "apply_modificator": "",
            "from_time": int(dt.timestamp()),
            "_": (time.time_ns() // 1_000_000)
        }
        print(params)

        url = f"https://pass.rw.by/ru/ajax/route/car_places/?{urllib.parse.urlencode(params)}"

        api_request_context = self.context.request
        response = await api_request_context.get(url)
        json_data = await response.json()
        with open(f"train{train.id}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        return json_data