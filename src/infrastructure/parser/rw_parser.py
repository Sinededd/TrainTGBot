import json
import os
import re
import time
import urllib.parse
from datetime import datetime
from typing import Dict

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import BrowserContext, expect

from domain.models.available_seats import Seat
from domain.models.tariffs import Tariffs
from domain.models.train import Train
from domain.exceptions import NoTrainsFoundException

load_dotenv()


class Parser:
    """Network parser for the Belarusian Railway website."""

    def __init__(self, context: BrowserContext):
        self.context = context
        self.train_page = None

    @staticmethod
    async def get_trains(station_from: str, station_to: str, date: str) -> list[Train]:
        train_list = []

        params = {
            "from": station_from,
            "from_exp": "",
            "from_esr": "",
            "to": station_to,
            "to_exp": "",
            "to_esr": "",
            "front_date": "",
            "date": date
        }

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://pass.rw.by/ru/route", params=params, headers=headers
            )
            html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

        trains = soup.select("div.sch-table__row-wrap.js-row")

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

        for train in trains:
            num_el = train.select_one(".train-number")
            train_number = num_el.get_text(strip=True) if num_el else ""

            route_el = train.select_one(".train-route")
            route = route_el.get_text(strip=True) if route_el else ""

            dep_time_el = train.select_one(".train-from-time")
            dep_time = dep_time_el.get_text(strip=True) if dep_time_el else ""

            dep_station_el = train.select_one(".train-from-name")
            dep_station = dep_station_el.get_text(strip=True) if dep_station_el else ""

            arr_time_el = train.select_one(".train-to-time")
            arr_time = arr_time_el.get_text(strip=True) if arr_time_el else ""

            arr_station_el = train.select_one(".train-to-name")
            arr_station = arr_station_el.get_text(strip=True) if arr_station_el else ""

            duration_el = train.select_one(".train-duration-time")
            duration = duration_el.get_text(strip=True) if duration_el else ""

            row_el = train.select_one(".sch-table__row")
            train_id = row_el.get("data-train-id", "") if row_el else ""

            tariffs = Tariffs()
            tickets = train.select(".sch-table__t-item")

            for ticket in tickets:
                type_el = ticket.select_one(".sch-table__t-name")
                type_val = ""

                if type_el and type_el.get_text(strip=True):
                    type_val = type_el.get_text(strip=True)
                elif ticket.select_one("i.svg-tag-bicycle--quantity"):
                    type_val = "Вело"

                type_val = type_val[:8]

                places_el = ticket.select_one(".sch-table__t-quant span")
                places = places_el.get_text(strip=True) if places_el else ""

                price_el = ticket.select_one(".ticket-cost")
                price = price_el.get_text(strip=True) if price_el else ""

                tariffs.add_tariff(type_val, places, price)

            train_obj = Train(
                train_number=train_number,
                date_=date,
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

        return train_list

    async def login(self):
        """Login the user on the website"""
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

    async def get_train_data(self, train_number: str, from_station: str, to_station: str, date: str,
                             time_: str) -> Dict:
        """Get JSON data of train, requires user authorization"""
        dt = datetime.strptime(
            f"{date} {time_}",
            "%Y-%m-%d %H:%M"
        )
        params = {
            "from": from_station,
            "to": to_station,
            "date": date,
            "train_number": train_number,
            "car_type": "2",
            # !!! Пользователь должен иметь возможно устанавливать приоритет  типов вагона или отключать ненужные
            "apply_modificator": "",
            "from_time": int(dt.timestamp()),
            "_": (time.time_ns() // 1_000_000)
        }
        print(params)

        url = f"https://pass.rw.by/ru/ajax/route/car_places/?{urllib.parse.urlencode(params)}"

        api_request_context = self.context.request
        response = await api_request_context.get(url)
        json_data = await response.json()
        with open(f"train{train_number}{date}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        return json_data

    async def choose_train(self, train_id: str, from_station: str, to_station: str, date: str) -> None:
        """Click chosen train, requires user authorization"""
        params = {
            "from": from_station,
            "from_exp": "",
            "from_esr": "",
            "to": to_station,
            "to_exp": "",
            "to_esr": "",
            "front_date": "",
            "date": date
        }
        url = f"https://pass.rw.by/ru/route?{urllib.parse.urlencode(params)}"

        self.train_page = await self.context.new_page()
        await self.train_page.goto(url)
        train_row = self.train_page.locator(f'.sch-table__row[data-train-id="{train_id}"]')
        await train_row.wait_for(state="visible", timeout=5000)
        await train_row.get_by_role("link", name="Выбрать места").click()
        await self.train_page.locator(".pl-accord__panel").first.wait_for(state="visible", timeout=10000)

    async def choose_seat(self, seat: Seat) -> None:
        """Click chosen seat of clicked train, requires to be clicked train"""
        target_carriage = f"Вагон №{seat.carNumber} ({seat.typeAbbr})"
        panel = self.train_page.locator(".pl-accord__panel").filter(has_text=target_carriage)
        await expect(panel).to_be_visible(timeout=5000)
        toggle_link = panel.locator(".pl-accord__acc-link")
        link_class = await toggle_link.get_attribute("class") or ""
        is_collapsed = "collapsed" in link_class
        if is_collapsed:
            print(f"Вагон '{target_carriage}' свернут. Разворачиваем...")
            await toggle_link.click()
            collapse_body = panel.locator(".pl-accord__collapse")
            await expect(collapse_body).to_have_class(re.compile(r"\bin\b"))

            preloader = panel.locator(".preloader")
            await expect(preloader).to_be_hidden()

            await panel.locator(".carriage__seats, canvas.carriage__canvas--inited").first.wait_for(state="visible")

            print("Вагон успешно раскрыт, схема мест загружена!")
        else:
            print(f"Вагон '{target_carriage}' уже был открыт.")
        await panel.locator(".carriage__seat-number").get_by_text(seat.number.lstrip("0"), exact=True).click()

    async def place_an_order(self, surname: str, name: str, patronymic: str, passNumber: str) -> None:
        await self.train_page.get_by_role("link", name="Ввести данные пассажиров").click()
        await self.train_page.get_by_role("textbox", name="Фамилия *").fill(surname)
        await self.train_page.get_by_role("textbox", name="Имя *").fill(name)
        await self.train_page.get_by_role("textbox", name="Отчество").fill(patronymic)
        await self.train_page.get_by_role("textbox", name="Номер документа *").fill(passNumber)
        await self.train_page.locator(".jq-checkbox").click()

        await self.train_page.pause()
        # await self.train_page.get_by_role("button", name="Оформить заказ").click()
