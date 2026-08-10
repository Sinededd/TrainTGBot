import urllib.parse
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

from src.models.tariffs import Tariffs
from src.models.train import Train
from services.parser import Parser


@pytest.mark.asyncio
@patch('time.time_ns')
async def test_check_available_seats(mock_time_ns):
    mock_time_ns.return_value = 1700000000000000000
    mock_timestamp_ms = str(1700000000000000000 // 1_000_000)

    mock_context = MagicMock()
    parser = Parser(context=mock_context)

    mock_repo = MagicMock()
    parser.trainRepository = mock_repo

    tariffs = Tariffs()
    mock_train = Train(
        train_number="701B",
        date_="2026-07-24",
        route="Minsk -> Brest",
        dep_time="19:30",
        dep_station="Minsk",
        arr_time="18:00",
        arr_station="Brest",
        duration="3h 30m",
        train_id="test_id_123",
        tariffs=tariffs
    )

    mock_repo.get_by_id.return_value = mock_train

    dt = datetime.strptime("2026-07-24 19:30", "%Y-%m-%d %H:%M")
    expected_from_time = str(int(dt.timestamp()))

    result_url = await parser.check_available_seats(train_id="test_id_123")

    # --- 3. ASSERT (Проверка результатов) ---

    # Проверяем, что репозиторий вызывался с правильным train_id
    mock_repo.get_by_id.assert_called_once_with("test_id_123")

    # Разбираем сгенерированный URL на параметры, чтобы проверить их
    print(result_url)
    parsed_url = urllib.parse.urlparse(result_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Проверяем базовую часть URL
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "pass.rw.by"
    assert parsed_url.path == "/ru/ajax/route/car_places/"

    # Проверяем query-параметры (parse_qs возвращает списки значений)
    assert query_params["from"][0] == "Minsk"
    assert query_params["to"][0] == "Brest"
    assert query_params["date"][0] == "2026-07-24"
    assert query_params["train_number"][0] == "701B"
    assert query_params["car_type"][0] == "2"
    assert query_params["from_time"][0] == expected_from_time
    assert query_params["_"][0] == mock_timestamp_ms