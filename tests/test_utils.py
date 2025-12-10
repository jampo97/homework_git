from src.utils import create_list_of_operations
import pytest
import os


@pytest.fixture()
def my_transactions() -> list:
    return [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на счет"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": None},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на счет"},
    ]


# Тест списка словарей с данными о транзакциях


# Тест списка словарей с данными о транзакциях
def test_create_list_of_operations(my_transactions:list) -> list:
    assert (
        create_list_of_operations(os.path.join(os.path.dirname(__file__), "..", "data", "operations.json"))
        == my_transactions
    )


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
