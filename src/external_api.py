import os

import requests
from dotenv import load_dotenv


def converter_currency(my_transaction: dict) -> float:
    """Конвертер валюты в рубли через API"""

    current_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории проекта
    file_path = os.path.join(current_dir, "..", ".env")  # Строим полный путь к файлу
    load_dotenv(file_path)  # запускаем файл .env
    API_KEY = os.getenv("API_KEY")  # В файле .env забираем апи_ключ

    start_amount: float = my_transaction["operationAmount"]["amount"]
    currency_code: str = my_transaction["operationAmount"]["currency"]["code"]

    # блок отвечающий за ошибки до вызова функции
    currency_to_convert = ["USD", "EUR"]  # допустимые валюты для ввода
    try:
        value = float(start_amount)
    except ValueError:
        raise ValueError("Некорректная сумма транзакции: невозможно преобразовать в число")

    if currency_code not in currency_to_convert:
        raise ValueError("Код валюты не поддерживается")

    if currency_code == "RUB":
        return float(start_amount)

    # запускаем готовый апи запрос
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={start_amount}"

    payload: dict = {}
    headers: dict = {"apikey": API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)

    # проверка на ошибки запроса
    if response.status_code != 200:
        raise ValueError(f"Ошибка запроса : {response.status_code}")
    amount: float = round(response.json()["result"], 2)
    return amount


if __name__ == "__main__":
    print(converter_currency({
        "id": 580054042,
        "state": "EXECUTED",
        "date": "2018-06-20T03:59:34.851630",
        "operationAmount": {
            "amount": "12334",
            "currency": {
                "name": "USD",
                "code": "RUB"
            }
        }}
    )
    )
