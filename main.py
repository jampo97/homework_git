import os

from src.csv_excel_reader import csv_reader, excel_reader
from src.utils import create_list_of_operations, process_bank_operations, process_bank_search
from src.widget import mask_account_card


def main() -> None:
    """Функция извлечения данных из файла их фильтрация и сортировка"""

    data = greeting()  # результат greeting - полный список транзакций

    filtered_data_1 = status_filter(data)  # результат status_filter - отфильтрованный список по статусу

    sorted_data = sort_by_date(filtered_data_1)  # результат sort_by_date - сортированный список по дате

    filtered_data_2 = rub_filter(sorted_data)  # результат rub_filter - отфильтрованный список по RUB

    filtered_data_3 = description_filter(filtered_data_2)  # результат description_filter - отфильтрованный список

    summary(filtered_data_3)  # результат summary - print списка после всех фильтров


def greeting() -> list[dict]:
    """Приветствие. Выбор файла"""

    while True:
        user_input = input(
            "Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n\n"
            "Выберите необходимый пункт меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла\n\n"
            "Пользователь: "
        )
        current_dir = os.path.dirname(__file__)
        if user_input == "1":
            file_path = os.path.join(current_dir, "data", "operations.json")
            print("Программа: Для обработки выбран JSON-файл.")
            data = create_list_of_operations(file_path)
            return data
        elif user_input == "2":
            file_path = os.path.join(current_dir, "data", "transactions.csv")
            print("Программа: Для обработки выбран CSV-файл.")
            data = csv_reader(file_path)
            return data
        elif user_input == "3":
            file_path = os.path.join(current_dir, "data", "transactions_excel.xlsx")
            print("Программа: Для обработки выбран XLSX-файл.")
            data = excel_reader(file_path)
            return data
        else:
            continue


def status_filter(data: list[dict]) -> list[dict]:
    """Фильтрация по статусу"""

    all_status = [transaction["state"] for transaction in data]  # Выводим список всех статусов
    all_status_list = list(set(all_status))  # Создаем множество - затем список

    while True:
        user_input = input(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {all_status_list}\n\n"
            "Пользователь: "
        )
        temp = True
        for i in range(len(all_status_list)):
            if user_input.upper() == all_status_list[i]:
                filtered_data = [transaction for transaction in data if transaction["state"] == all_status_list[i]]
                temp = False  # Условие выхода из вложенного цикла
                print(f"Операции отфильтрованы по статусу {user_input.upper()}")
                return filtered_data
            elif user_input.upper() in all_status_list:
                continue
            else:
                print(f"Программа: Статус операции {user_input} недоступен.")
                break
        if temp:
            continue
        else:
            break


def sort_by_date(filtered_data_1: list[dict]) -> list[dict]:
    """Сортировка по дате"""

    user_input = input("Программа: Отсортировать по дате? Y/N\n" "Пользователь: ")
    if user_input == "Y":
        user_input = input("Программа: Отсортировать по возрастанию? Y/N\n" "Пользователь: ")
        if user_input == "Y":
            sorted_data = sorted(filtered_data_1, key=lambda transaction: transaction["date"])
            print("Операции отфильтрованы по возрастанию даты")
        else:
            sorted_data = sorted(filtered_data_1, key=lambda transaction: transaction["date"], reverse=True)
            print("Операции отфильтрованы по убыванию даты")
    else:
        sorted_data = filtered_data_1
    return sorted_data


def rub_filter(sorted_data: list[dict]) -> list[dict]:
    """Фильтрация по рублевым операциям"""

    user_input = input("Программа: Выводить только рублевые транзакции? Y/N\n" "Пользователь: ")
    if user_input == "Y":
        filtered_data_2 = list(
            filter(lambda transaction: transaction["operationAmount"]["currency"]["code"] == "RUB", sorted_data)
        )
        print("Будут выведены только рублевые транзакции")
    else:
        filtered_data_2 = sorted_data
    return filtered_data_2


def description_filter(filtered_data_2: list[dict]) -> list[dict]:
    """Фильтрация по описанию"""

    while True:
        user_input = input(
            "Программа: Отфильтровать список транзакций по определенному слову в описании? Y/N\n" "Пользователь: "
        )
        if user_input == "Y":
            user_input = input("Программа: Введите слово\n" "Пользователь: ")
            if user_input in ", ".join(process_bank_operations(filtered_data_2,
                                                               ["Перевод организации", "Открытие вклада",
                                                                "Перевод со счета на счет",
                                                                "Перевод с карты на карту",
                                                                "Перевод с карты на счет"])):
                filtered_data_3 = process_bank_search(filtered_data_2, user_input)

                print(f"Список транзакций отфильтрован по слову {user_input}")
                return filtered_data_3
            else:
                print(f"Список транзакций не может быть отфильтрован по слову {user_input}")
            continue
        else:
            filtered_data_3 = filtered_data_2
        return filtered_data_3


def summary(filtered_data_3: list[dict]):
    """Итого"""
    if len(filtered_data_3) == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(
            "Программа: Распечатываю итоговый список транзакций...\n"
            f"Программа:Всего банковских операций в выборке: {len(filtered_data_3)}\n"
        )
    for transaction in filtered_data_3:
        print(transaction["date"] + " " + transaction["description"])  # дата и описание транзакции
        if "from" in transaction:  # Условие наличия отправителя
            print(mask_account_card(transaction["from"]) + "->" + mask_account_card(transaction["to"]))
        else:
            print(mask_account_card(transaction["to"]))
        print(
            f'Сумма:{transaction["operationAmount"]["amount"]}'
            f' {transaction["operationAmount"]["currency"]["name"]}\n'
        )
    return True


if __name__ == "__main__":
    main()
