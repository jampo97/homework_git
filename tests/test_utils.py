import json
import os
from unittest.mock import Mock

from src.utils import create_list_of_operations


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

def test_create_list_of_operations():
    my_mock = Mock(return_value=[{"description": "Взятка"}, {"description": "Зарплата"}])
    json.load = my_mock
    assert create_list_of_operations(os.path.join(os.path.dirname(__file__), "..", "data", "empty.json")) == [
        {"description": "Взятка"}, {"description": "Зарплата"}]
