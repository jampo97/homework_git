import os
import zipfile
from unittest.mock import patch

import pandas as pd
import pytest
from pandas import DataFrame, Series
from pandas.errors import EmptyDataError

from src.csv_excel_reader import csv_reader, errors_in_df, excel_reader, to_dict_type


@pytest.fixture()
def my_transaction_ser() -> Series:
    return pd.Series(
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "description": "Перевод организации",
            "from": "Счет 58803664561298323391",
            "to": "Счет 97415660563456619397",
        }
    )


@pytest.fixture()
def my_transaction_ser_empty() -> Series:
    return pd.Series(
        {
            "id": "",
            "state": "",
            "date": "",
            "amount": "",
            "currency_name": "",
            "currency_code": "",
            "description": "",
            "from": "",
            "to": "",
        }
    )


@pytest.fixture()
def my_transaction_df() -> DataFrame:
    return pd.DataFrame(
        {
            "id": [650703, 33],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-09-05T11:30:32Z", "2021-09-05T11:30:32Z"],
            "amount": [16210, 33],
            "currency_name": ["Sol", "USD"],
            "currency_code": ["PEN", "USD"],
            "from": ["Счет 58803664561298323391", "Счет 97415660563456619397"],
            "to": ["Счет 97415660563456619397", "Счет 58803664561298323391"],
            "description": ["Перевод организации", "Перевод со счета на счет"],
        }
    )


@pytest.fixture()
def my_transaction_list() -> list:
    return [
        {
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод организации",
            "from": "Счет 58803664561298323391",
            "id": "650703",
            "operationAmount": {"amount": "16210", "currency": {"code": "PEN", "name": "Sol"}},
            "state": "EXECUTED",
            "to": "Счет 97415660563456619397",
        },
        {
            "date": "2021-09-05T11:30:32Z",
            "description": "Перевод со счета на счет",
            "from": "Счет 97415660563456619397",
            "id": "33",
            "operationAmount": {"amount": "33", "currency": {"code": "USD", "name": "USD"}},
            "state": "EXECUTED",
            "to": "Счет 58803664561298323391",
        },
    ]


# Тест файла csv при нормальном вводе
@patch("pandas.read_csv")  # функция "pandas.read_csv" заменится на заглушку
def test_csv_reader(
    mock_read_csv,  # заглушка - переменная "mock_read_csv"
    my_transaction_df,  # добавим фикстуру со значениями таблицы
    my_transaction_list,
) -> None:  # добавим фикстуру со списком словарей на выходе
    mock_data = my_transaction_df  # задаем значение для переменной "mock_data" = значениям таблицы
    mock_read_csv.return_value = mock_data  # присваиваем выходные значения заглушки
    assert (
        csv_reader("любой адрес") == my_transaction_list
    )  # Тест "csv_reader" (аргумент любой, так как ниже стоит заглушка)


# Тест файла excel при нормальном вводе
@patch("pandas.read_excel")
def test_excel_reader(mock_read_excel, my_transaction_df: DataFrame, my_transaction_list: list) -> None:
    mock_data = my_transaction_df
    mock_read_excel.return_value = mock_data
    assert excel_reader("любой адрес") == my_transaction_list


# Тест если файл не найден
def test_csv_excel_reader_not_found_file() -> None:
    with pytest.raises(FileNotFoundError) as e:
        csv_reader(os.path.join(os.path.dirname(__file__), "..", "data", "no_transactions.csv"))
    with pytest.raises(FileNotFoundError) as e:
        excel_reader(os.path.join(os.path.dirname(__file__), "..", "data", "no_transactions_excel.xlsx"))
    assert str(e.value) == "Файл не найден"


# Тест если файл csv пустой
def test_csv_reader_empty_file() -> None:
    with pytest.raises(EmptyDataError) as e:
        csv_reader(os.path.join(os.path.dirname(__file__), "..", "data", "empty.json"))
    assert str(e.value) == "Файл пустой"


# Тест Ошибка кодировки/Неверный тип файла
def test_csv_reader_error_file() -> None:
    with pytest.raises(Exception) as e:
        csv_reader(os.path.join(os.path.dirname(__file__), "..", "data", "transactions_excel.xlsx"))
    assert str(e.value) == "Файл не открывается"


# Тест если файл excel пустой или просто не открывается
def test_excel_reader_empty_file() -> None:
    with pytest.raises(zipfile.BadZipFile) as e:
        excel_reader(os.path.join(os.path.dirname(__file__), "..", "data", "empty.json"))
    assert str(e.value) == "Файл не открывается"


# Тест перевода список в словарь при нормальном вводе
def test_to_dict(my_transaction_ser: Series) -> None:
    assert to_dict_type(my_transaction_ser) == {
        "date": "2023-09-05T11:30:32Z",
        "description": "Перевод организации",
        "from": "Счет 58803664561298323391",
        "id": "650703",
        "operationAmount": {"amount": "16210", "currency": {"code": "PEN", "name": "Sol"}},
        "state": "EXECUTED",
        "to": "Счет 97415660563456619397",
    }


# Тест перевода список в словарь при пустых значениях
def test_to_dict_empty(my_transaction_ser_empty: Series) -> None:
    assert to_dict_type(my_transaction_ser_empty) == {
        "id": "",
        "state": "",
        "date": "",
        "operationAmount": {"amount": "", "currency": {"name": "", "code": ""}},
        "description": "",
        "from": "",
        "to": "",
    }


# Тест проверки ошибок в строке
def test_errors_in_df(capsys, my_transaction_ser):
    transaction = my_transaction_ser.copy()
    transaction["id"] = "abc"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка данных. Строка - 1, столбец - id\n" in captured.out

    transaction["state"] = "abc"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка типа данных. Строка - 1, столбец - state\n" in captured.out

    transaction["date"] = "2020-12-06T23:00:58"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка данных. Строка - 1, столбец - date\n" in captured.out

    transaction["amount"] = "abc"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка типа данных. Строка - 1, столбец - amount\n" in captured.out

    transaction["currency_name"] = "1USD"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка типа данных. Строка - 1, столбец - currency_name\n" in captured.out

    transaction["currency_code"] = "USDT"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка типа данных. Строка - 1, столбец - currency_code\n" in captured.out

    transaction["to"] = "1234567890123456"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Пожалуйста, укажите название карты в начале. Строка - 1, столбец - to\n" in captured.out

    transaction["to"] = "1"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка типа данных. Строка - 1, столбец - to\n" in captured.out

    transaction["to"] = "Абв 12345678901234567890"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Не введено слово Счет. Строка - 1, столбец - to\n" in captured.out

    transaction["description"] = "abc"  # Некорректное значение для проверки
    errors_in_df(transaction, 0)
    captured = capsys.readouterr()
    assert "Ошибка типа данных. Строка - 1, столбец - description\n" in captured.out
