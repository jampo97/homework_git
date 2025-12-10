import os
from dotenv import load_dotenv
import requests


def converter_currency(my_transaction: dict) -> float:
    """Конвертер валюты в рубли через API"""

    current_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории проекта
    file_path = os.path.join(current_dir, "..", ".env")  # Строим полный путь к файлу
    load_dotenv(file_path)  # запускаем файл .env
    API_KEY = os.getenv("API_KEY")  # В файле .env забираем апи_ключ

    money: float = my_transaction["money"]
    currency: str = my_transaction["currency"]

    # блок отвечающий за ошибки до вызова функции
    currency_to_convert = ["USD", "EUR"]  # допустимые валюты для ввода
    if not isinstance(money, (int, float)):  # Условие ввода транзакции
        print("Введена неверная сумма транзакции")
        return False

    elif my_transaction["currency"] not in currency_to_convert:  # условие ввода валюты
        print("Такой валюты нет в списке")
        return False

    else:
        # запускаем готовый апи запрос
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={money}"

        payload: dict = {}
        headers: dict = {"apikey": API_KEY}

        response = requests.request("GET", url, headers=headers, data=payload)

        # проверка на ошибки запроса
        if response.status_code != 200:
            print(f"Ошибка запроса : {response.status_code}")
            return False
        amount: float = round(response.json()["result"], 2)
        return amount


if __name__ == "__main__":
    print(converter_currency({"money": 1000,
                              "currency": "USD"
                              }))
