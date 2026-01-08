from unittest.mock import patch

import pytest

from main import description_filter, greeting, rub_filter, sort_by_date, status_filter, summary


@pytest.fixture()
def data() -> list[dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 587085106,
            "state": "PENDING",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


@pytest.fixture()
def data_sorted_by_date() -> list[dict]:
    return [
        {
            "id": 587085106,
            "state": "PENDING",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


@pytest.fixture()
def data_sorted_by_date_r() -> list[dict]:
    return [
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 587085106,
            "state": "PENDING",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
    ]


@pytest.fixture()
def only_pending_rub() -> list[dict]:
    return [
        {
            "id": 587085106,
            "state": "PENDING",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        }
    ]


# Тесты открытия файла


@patch("builtins.input", side_effect=["1"])
def test_greeting_json_output(mock_input, capsys):
    greeting()
    captured = capsys.readouterr()
    assert "Программа: Для обработки выбран JSON-файл." in captured.out


@patch("builtins.input", side_effect=["2"])
def test_greeting_csv_output(mock_input, capsys):
    greeting()
    captured = capsys.readouterr()
    assert "Программа: Для обработки выбран CSV-файл." in captured.out


@patch("builtins.input", side_effect=["3"])
def test_greeting_excel_output(mock_input, capsys):
    greeting()
    captured = capsys.readouterr()
    assert "Программа: Для обработки выбран XLSX-файл." in captured.out


# Тесты фильтра STATE


@patch("builtins.input", side_effect=["pending"])
def test_status_filter(mock_input, data, only_pending_rub):
    assert status_filter(data) == only_pending_rub


@patch("builtins.input", side_effect=["EXECUTED"])
def test_status_filter_output(mock_input, capsys, data):
    status_filter(data)
    captured = capsys.readouterr()
    assert "Операции отфильтрованы по статусу EXECUTED" in captured.out


# Тесты сортировки по дате


@patch("builtins.input", side_effect=["Y", "Y"])
def test_sort_by_date_y(mock_input, data, data_sorted_by_date):
    assert sort_by_date(data) == data_sorted_by_date


@patch("builtins.input", side_effect=["Y", "Y"])
def test_sort_by_date_y_output(mock_input, capsys, data):
    sort_by_date(data)
    captured = capsys.readouterr()
    assert "Операции отфильтрованы по возрастанию даты\n" in captured.out


@patch("builtins.input", side_effect=["Y", "N"])
def test_sort_by_date_r(mock_input, data, data_sorted_by_date_r):
    assert sort_by_date(data) == data_sorted_by_date_r


@patch("builtins.input", side_effect=["Y", "N"])
def test_sort_by_date_r_output(mock_input, capsys, data):
    sort_by_date(data)
    captured = capsys.readouterr()
    assert "Операции отфильтрованы по убыванию даты\n" in captured.out


@patch("builtins.input", side_effect=["N"])
def test_sort_by_date_n(mock_input, data, data_sorted_by_date):
    assert sort_by_date(data) == data


# Тесты фильтра рублевых операций


@patch("builtins.input", side_effect=["Y"])
def test_rub_filter(mock_input, data, only_pending_rub):
    assert rub_filter(data) == only_pending_rub


@patch("builtins.input", side_effect=["Y"])
def test_rub_filter_output(mock_input, capsys, data):
    rub_filter(data)
    captured = capsys.readouterr()
    assert "Будут выведены только рублевые транзакции\n" in captured.out


@patch("builtins.input", side_effect=["N"])
def test_rub_filter_no(mock_input, data):
    assert rub_filter(data) == data


# Тесты фильтра по описанию


@patch("builtins.input", side_effect=["Y", "вклад"])
def test_description_filter(mock_input, data, only_pending_rub):
    assert description_filter(data) == only_pending_rub


@patch("builtins.input", side_effect=["Y", "вклад"])
def test_description_filter_output(mock_input, capsys, data):
    description_filter(data)
    captured = capsys.readouterr()
    assert "Список транзакций отфильтрован по слову вклад\n" in captured.out


@patch("builtins.input", side_effect=["N"])
def test_description_filter_n(mock_input, data):
    assert description_filter(data) == data


# Тесты итогового вывода данных


def test_summary_empty(capsys):
    summary([])
    captured = capsys.readouterr()
    assert (
        "Программа: Распечатываю итоговый список транзакций...\n"
        "Программа:Всего банковских операций в выборке: 0\n" in captured.out
    )


def test_summary(capsys, only_pending_rub):
    summary(only_pending_rub)
    captured = capsys.readouterr()
    assert (
        "Программа: Распечатываю итоговый список транзакций...\n"
        "Программа:Всего банковских операций в выборке: 1\n"
        "\n"
        "2018-03-23T10:45:06.972075 Открытие вклада\n"
        "Счет **2431\n"
        "Сумма:48223.05 руб.\n"
        "\n" in captured.out
    )
