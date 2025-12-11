import json
import logging
import os

my_logger = logging.getLogger("utils")
my_logger.setLevel(logging.INFO)
log_filename = os.path.join(os.path.dirname(__file__), "..", "logs", "utils.log")
file_handler = logging.FileHandler(log_filename, 'w', encoding="utf-8")
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
    # list_of_operations = [{"description": operation.get("description")} for operation in data]
    list_of_operations = [operation for operation in data]
    my_logger.info("Создан список словарей с транзакциями")
    return list_of_operations


if __name__ == "__main__":
    # Получаем путь к текущей директории проекта
    current_dir = os.path.dirname(__file__)

    # Строим полный путь к файлу
    file_path = os.path.join(current_dir, "..", "data", "operations.json")
    print(create_list_of_operations(file_path))
