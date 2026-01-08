import json
import logging
import os
import re
from collections import Counter

my_logger = logging.getLogger("utils")
my_logger.setLevel(logging.INFO)
log_filename = os.path.join(os.path.dirname(__file__), "..", "logs", "utils.log")
file_handler = logging.FileHandler(log_filename, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)


def create_list_of_operations(source_to_operations: str) -> list:
    """Функция возвращает список словарей с данными о финансовых транзакциях"""

    my_logger.info("Запуск функции create_list_of_operations")
    list_of_operations: list = []
    try:
        my_logger.info(f"открываем файл {source_to_operations}")
        with open(source_to_operations, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print("Ошибка декодирования")
                my_logger.error(f" Возникла ошибка декодирования {e}")
                return list_of_operations
    except FileNotFoundError as e:
        print("Файл не найден")
        my_logger.error(f"Файл не найден. Ошибка {e}")
        return list_of_operations
    my_logger.info("ошибок не обнаружено")

    list_of_operations = [operation for operation in data]
    list_of_operations = list(filter(None, list_of_operations))
    my_logger.info("Создан список словарей с транзакциями")
    return list_of_operations


def process_bank_search(data: list[dict], search: str = "USD") -> list[dict]:
    """Поиск транзакций содержащих слово"""

    pattern = rf"{search}"
    finder = [transaction for transaction in data if re.findall(pattern, ", ".join(dict_to_list(transaction)))]

    return finder


def dict_to_list(my_dict: dict) -> list[str]:
    """Значения словаря выводим в список"""

    finder = []
    for value in my_dict.values():
        if type(value) is dict:
            finder.extend(dict_to_list(value))
        else:
            finder.append(str(value))
    finder_list = [str(item) for item in finder]  # переводим тип всех значений в string
    return finder_list


def process_bank_operations(data: list[dict]) -> dict:
    """Счетчик категорий операций"""
    descriptions = [transaction.get("description") for transaction in data]
    new_dict = dict(Counter(descriptions))
    return new_dict


if __name__ == "__main__":
    # Получаем путь к текущей директории проекта
    current_dir = os.path.dirname(__file__)

    # Строим полный путь к файлу
    file_path = os.path.join(current_dir, "..", "data", "operations.json")
    print(create_list_of_operations(file_path))
    print(process_bank_search(create_list_of_operations(file_path)))
    print(process_bank_operations(create_list_of_operations(file_path)))
