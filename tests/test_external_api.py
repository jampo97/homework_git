import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

from src.external_api import converter_currency

current_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории проекта
file_path = os.path.join(current_dir, "..", ".env")  # Строим полный путь к файлу
load_dotenv(file_path)  # запускаем файл .env
API_KEY = os.getenv("API_KEY")  # В файле .env забираем апи_ключ


# Тест с ошибкой при вводе валюты
def test_converter_currency_err_cur() -> None:
    with pytest.raises(ValueError) as no_cur:
        converter_currency(
            {
                "id": 580054042,
                "state": "EXECUTED",
                "date": "2018-06-20T03:59:34.851630",
                "operationAmount": {"amount": "12334", "currency": {"name": "USD", "code": "UD"}},
            }
        )
    assert str(no_cur.value) == "Код валюты не поддерживается"


# Тест с ошибкой при вводе суммы транзакции
def test_converter_currency_err_trans() -> None:
    with pytest.raises(ValueError) as no_cur:
        converter_currency(
            {
                "id": 580054042,
                "state": "EXECUTED",
                "date": "2018-06-20T03:59:34.851630",
                "operationAmount": {"amount": "abc", "currency": {"name": "USD", "code": "USD"}},
            }
        )
    assert str(no_cur.value) == "Некорректная сумма транзакции: невозможно преобразовать в число"


# Тест где патчим АПИ
@patch("requests.request")
def test_converter_currency(mock_get):
    mock_get.return_value.json.return_value = {"result": 5}
    mock_get.return_value.status_code = 200
    assert (
        converter_currency(
            {
                "id": 580054042,
                "state": "EXECUTED",
                "date": "2018-06-20T03:59:34.851630",
                "operationAmount": {"amount": "1000", "currency": {"name": "USD", "code": "USD"}},
            }
        )
        == 5
    )
    mock_get.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1000.0",
        headers={"apikey": API_KEY},
        data={},
    )
