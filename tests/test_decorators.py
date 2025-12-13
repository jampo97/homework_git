from src.decorators import my_function


# тест вывода в консоль при нормальном вводе
def test_log(capsys):
    my_function(2, 2)
    captured = capsys.readouterr()
    assert captured.out.splitlines()[0] == "Имя функции: my_function,"
    assert captured.out.splitlines()[1] == "Аргументы x и у = 2 и 2,"
    assert captured.out.splitlines()[3] == "___________"
    assert captured.out.splitlines()[4] == "Результат выполнения функции:"
    assert captured.out.splitlines()[5] == ""
    assert captured.out.splitlines()[6] == "1.0"
    assert captured.out.splitlines()[7] == ""
    assert captured.out.splitlines()[8] == "__________"


# тест вывода в консоль при неверном количестве аргументов
def test_log_err_arg(capsys):
    my_function(2, 2, 3, 5)
    captured = capsys.readouterr()
    assert captured.out == "Введено неверное количество аргументов - 4\n"


# тест вывода в консоль при неверном типе аргументов
def test_log_err(capsys):
    my_function(5, "S")
    captured = capsys.readouterr()
    assert captured.out == "Введите 2 числа. Вы ввели 5 и S\n"


# тест вывода в консоль при делителе равном 0
def test_log_zero(capsys):
    # with pytest.raises(ZeroDivisionError, match="Ошибка: деление на ноль недопустимо"):
    my_function(5, 0)
    captured = capsys.readouterr()
    assert captured.out == "Ошибка: деление на ноль недопустимо\n"
