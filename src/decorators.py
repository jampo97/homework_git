from functools import wraps
from time import time


# декоратор логи с параметром - файл, в котором будут сохранения
def log(filename=None):
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args):

            # начало работы декоратора
            start_time = time()

            # блок отвечающий за ошибки до вызова функции
            if len(args) != 2:
                print(f"Введено неверное количество аргументов - {len(args)}")
                return None

            # блок отвечающий за ошибки при вызове функции
            try:
                result = func(*args)
            except TypeError:
                print(f"Введите 2 числа. Вы ввели {args[0]} и {args[1]}")
                return None
            except ZeroDivisionError:
                print("Ошибка: деление на ноль недопустимо")
                return None

            # приводим значения для логов
            log_1 = (
                f"Имя функции: {my_function.__name__},\n"
                f"Аргументы x и у = {args[0]} и {args[1]},\n"
                f"Время начала функции: {start_time},"
                f"\n___________\n"
                f"Результат выполнения функции:\n"
            )

            log_2 = f"\n__________\n" f"Время конца функции: {time()}"

            # блок для вывода текста в консоль
            if filename is None or filename == "":

                print(log_1)
                print(str(result))
                print(log_2)

            # блок для вывода текста в файл
            else:
                with open(filename, "w", encoding="utf--8") as file:
                    file.write(log_1)
                    file.write(str(result))
                    file.write(log_2)

            return result

        return wrapper

    return my_decorator


@log()
def my_function(x: float, y: float) -> float:
    """Функция деления"""
    return x / y


my_function(2, 1)
