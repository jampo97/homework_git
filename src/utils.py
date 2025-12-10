import json
import os


def create_list_of_operations(source_to_operations: str) -> list:
    """Функция возвращает список словарей с данными о финансовых транзакциях"""

    list_of_operations: list = []
    try:
        with open(source_to_operations, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка декодирования")
                return list_of_operations
    except FileNotFoundError:
        print("Файл не найден")
        return list_of_operations

    list_of_operations = [{"description": operation.get("description")} for operation in data]
    # list_of_operations = [operation for operation in data]

    return list_of_operations


if __name__ == "__main__":
    # Получаем путь к текущей директории проекта
    current_dir = os.path.dirname(__file__)

    # Строим полный путь к файлу
    file_path = os.path.join(current_dir, "..", "data", "operations.json")
    print(create_list_of_operations(file_path))
