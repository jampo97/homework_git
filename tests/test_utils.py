import json
import os
from unittest.mock import Mock

import pytest

from src.utils import create_list_of_operations, dict_to_list, process_bank_operations, process_bank_search


# Тест если файл не найден
def test_create_list_of_operations_err_file(capsys):
    create_list_of_operations("/data/operations.json")
    captured = capsys.readouterr()
    assert captured.out == "Файл не найден\n"


# Тест если файл пустой
def test_create_list_of_operations_empty(capsys):
    create_list_of_operations(os.path.join(os.path.dirname(__file__), "..", "data", "empty.json"))
    captured = capsys.readouterr()
    assert captured.out == "Ошибка декодирования\n"


# Тест списка словарей с данными о транзакциях (замоканный)
def test_create_list_of_operations() -> None:
    my_mock = Mock(return_value=[{"description": "Взятка"}, {"description": "Зарплата"}])
    json.load = my_mock
    assert create_list_of_operations(os.path.join(os.path.dirname(__file__), "..", "data", "empty.json")) == [
        {"description": "Взятка"},
        {"description": "Зарплата"},
    ]


# Тест перевода значений словаря в список
@pytest.mark.parametrize(
    "dict, finder_list",
    [
        ({"1": "RUB", "2": "USD", "3": "EUR"}, ["RUB", "USD", "EUR"]),
        ({"1": "RUB", "2": "USD", "3": {"3_1": "Rub", "3_2": "Euro"}}, ["RUB", "USD", "Rub", "Euro"]),
        ({"1": "", "2": "USD", "3": "EUR"}, ["", "USD", "EUR"]),
    ],
)
def test_dict_to_list(dict, finder_list) -> None:
    assert dict_to_list(dict) == finder_list


# Тест счетчика категорий операций
def test_process_bank_operations() -> None:
    mock_data = [
        {"description": "Перевод со счета на счет"},
        {"description": "Открытие вклада"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
    ]

    assert process_bank_operations(mock_data) == {
        "Перевод со счета на счет": 2,
        "Открытие вклада": 1,
        "Перевод с карты на карту": 1,
    }


# Тест поиска транзакций содержащих определенное слово
def test_process_bank_search() -> None:
    mock_data = [{"1": "USD получка"}, {"2": "EUR"}, {"3": "RUB"}, {"4": "перевод USD"}]
    assert process_bank_search(mock_data, "USD") == [
        {"1": "USD получка"},
        {"4": "перевод USD"},
    ]
