from unittest.mock import patch
import os

from dotenv import load_dotenv

from src.external_api import converter_currency

current_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории проекта
file_path = os.path.join(current_dir, "..", ".env")  # Строим полный путь к файлу
load_dotenv(file_path)  # запускаем файл .env
API_KEY = os.getenv("API_KEY")  # В файле .env забираем апи_ключ


# Тест с ошибкой при вводе валюты
def test_converter_currency_err_cur(capsys):
    converter_currency(1000, "qq")
    captured = capsys.readouterr()
    assert captured.out == "Такой валюты нет в списке\n"


# Тест с ошибкой при вводе суммы транзакции
def test_converter_currency_err_trans(capsys):
    converter_currency([1000], "USD")
    captured = capsys.readouterr()
    assert captured.out == "Введена неверная сумма транзакции\n"


# Тест где мокаем АПИ
@patch("requests.request")
def test_converter_currency(mock_get):
    mock_get.return_value.json.return_value = {"result": 5}
    mock_get.return_value.status_code = 200
    assert converter_currency(8, "USD") == 5
    mock_get.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8",
        headers={"apikey": API_KEY},
        data={},
    )
