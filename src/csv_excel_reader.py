import os
import zipfile
from datetime import datetime

import pandas as pd
from pandas import DataFrame, Series
from pandas.errors import EmptyDataError


def csv_reader(source_to_operations: str) -> list[dict]:
    """Функция преобразования файла типа .csv в список словарей с транзакциями"""

    all_transactions: list = []
    try:
        df_all = pd.read_csv(source_to_operations, delimiter=";")  # открываем файл csv в формате dataframe
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    except EmptyDataError:
        raise EmptyDataError("Файл пустой")
    except Exception:
        raise Exception("Файл не открывается")

    search_empty_row(df_all)  # поиск и удаление пустых строк

    for x in range(len(df_all)):  # запускаем цикл преобразования таблицы в список словарей
        transaction = df_all.iloc[x]  # обращаемся к строке с индексом "х"
        errors_in_df(transaction, x)  # Поиск ошибок при чтении значений и запись их перед выводом транзакций
        all_transactions.append(to_dict_type(transaction))  # добавляем словарь в список
    return all_transactions


def excel_reader(source_to_operations: str) -> list[dict]:
    """Функция преобразования excel файла в список словарей с транзакциями"""

    all_transactions: list = []
    try:
        df_all = pd.read_excel(source_to_operations, engine="openpyxl")  # открываем файл excel в формате dataframe
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    except zipfile.BadZipFile:
        raise zipfile.BadZipFile("Файл не открывается")

    search_empty_row(df_all)  # поиск и удаление пустых строк

    for x in range(len(df_all)):  # запускаем цикл преобразования таблицы в список словарей
        transaction = df_all.iloc[x]  # обращаемся к строке с индексом "х"
        errors_in_df(transaction, x)  # Поиск ошибок при чтении значений и запись их перед выводом транзакций
        all_transactions.append(to_dict_type(transaction))  # добавляем словарь в список
    return all_transactions


def to_dict_type(transaction: Series) -> dict:
    """Функция преобразования строки датафрейма в словарь"""
    my_dict = {
        "id": str(transaction["id"]),
        "state": str(transaction["state"]),
        "date": str(transaction["date"]),
        "operationAmount": {
            "amount": str(transaction["amount"]),
            "currency": {"name": str(transaction["currency_name"]), "code": str(transaction["currency_code"])},
        },
        "description": str(transaction["description"]),
        "from": str(transaction["from"]),
        "to": str(transaction["to"]),
    }
    return my_dict


def search_empty_row(df_all) -> DataFrame:
    """Поиск и удаление пустых строк"""

    # запускаем цикл преобразования таблицы в список словарей
    for x in range(len(df_all)):
        transaction = df_all.iloc[x]  # обращаемся к строке с индексом "х"

        # проверка пустых строк
        nan_columns = df_all.columns[transaction.isna()]  # Возвращаем имена столбцов [в этой строке.у которых NaN]
        if not nan_columns.empty:  # проверяем пуст ли список имен столбцов
            for column_name in nan_columns:
                if column_name not in ["from"]:  # исключаем столбец "from"
                    print(f"Не введены данные в строке - {x + 1}, столбец - {column_name}")

    return df_all.dropna(
        subset=["id", "state", "date", "amount", "currency_name", "currency_code", "to", "description"], inplace=True
    )


def errors_in_df(transaction: Series, x: int) -> None:
    """Поиск ошибок при чтении значений"""

    # проверка 1 столбца на наличие неверных данных
    try:
        float(transaction["id"])
    except ValueError:
        print(f"Ошибка данных. Строка - {x + 1}, столбец - id")

    # проверка 2 столбца на наличие неверных данных
    if transaction["state"] not in ["EXECUTED", "CANCELED", "PENDING"]:
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - state")

    # проверка 3 столбца на наличие неверных данных
    try:
        datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        print(f"Ошибка данных. Строка - {x + 1}, столбец - date")
    except TypeError:
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - date")

    # проверка 4 столбца на наличие неверных данных
    try:
        float(transaction["amount"])
    except ValueError:
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - amount")

    # проверка 5 столбца на наличие неверных данных
    no_whitespace = "".join(transaction["currency_name"].split())  # удаляем пробелы из строки
    if not no_whitespace.isalpha():
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - currency_name")

    # проверка 6 столбца на наличие неверных данных
    if not transaction["currency_code"].isupper() or len(transaction["currency_code"]) != 3:
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - currency_code")

    # проверка 8 столбца на наличие неверных данных
    count_num_in_account: int = 20
    count_num_in_card: int = 16
    counter = sum(1 for item in transaction["to"] if item.isnumeric())

    if counter == count_num_in_account:  # 1 условие проверки для корректного ввода номера счета
        if "Счет " not in transaction["to"][0:5]:  # 2 условие проверки для ввода слова "Счет "
            print(f"Не введено слово Счет. Строка - {x + 1}, столбец - to")

    elif counter == count_num_in_card:  # 1 условие проверки для корректного ввода номера карты
        if not transaction["to"][0].isalpha():  # условие проверки названия карты
            print(f"Пожалуйста, укажите название карты в начале. Строка - {x + 1}, столбец - to")

    elif counter != count_num_in_account and counter != count_num_in_card:
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - to")

    # проверка 9 столбца на наличие неверных данных
    if transaction["description"] not in [
        "Перевод организации",
        "Перевод с карты на карту",
        "Открытие вклада",
        "Перевод со счета на счет",
    ]:
        print(f"Ошибка типа данных. Строка - {x + 1}, столбец - description")
    return None


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории проекта

    # Строим полный путь к файлу

    # file_path = os.path.join(current_dir, "..", "data", "transactions.csv")
    file_path = os.path.join(current_dir, "..", "data", "transactions_excel.xlsx")
    # # print(csv_reader(file_path))
    print(excel_reader(file_path))
