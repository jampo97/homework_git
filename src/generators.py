from typing import Generator, Iterator


def filter_by_currency(transactions: list[dict], currency: str | None = "USD"):
    """Функция фильтрует транзакции, где валюта операции соответствует заданной (например, USD)."""

    # Создаем генератор транзакций с условием определенной валюты
    filtered_transactions: Generator = (transaction for transaction in transactions
                                        if transaction["operationAmount"]["currency"]["code"] == currency)

    # записываем определенное количество отфильтрованных транзакций
    for filtered_transaction in range(3):  #
        print(next(filtered_transactions))


def transaction_descriptions(transactions: list[dict]):
    """ Генераторная функция, которая возвращает описание каждой операции по очереди. """
    # Создаем генератор описания транзакций
    descriptions_transactions: Generator = (transaction["description"] for transaction in transactions)

    # записываем определенное количество описаний транзакций
    for descriptions_transaction in range(5):
        print(next(descriptions_transactions))


def card_number_generator(start: str, end: str):
    """Функция-генератор номера карты"""
    card_number:str = "0000000000000000"

    for iteration in range(int(end) - int(start)):  # количество итераций (номеров карт)

        start = str(int(start) + 1)  # счетчик + номер карты
        form_cards: str = ""

        card_number = "0" * (len(card_number) - len(start)) + start # преобразование в 16-значное число

        for i, num in enumerate(card_number): # преобразование в формат хххх хххх хххх хххх
            if i > 3 and i % 4 == 0:
                form_cards += " "
            form_cards += num

        print(form_cards)


my_transactions = (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)

filter_by_currency(my_transactions, "USD")
transaction_descriptions(my_transactions)
card_number_generator("10000000000", "10000000011")
