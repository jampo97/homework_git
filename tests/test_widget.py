import pytest

from src.widget import account_or_card, get_date, mask_account_card


@pytest.fixture()
def user_text_card():
    return ["Maestro 1596837868705199", "Visa Classic 6831982476737658"]

@pytest.fixture()
def user_text_acc():
    return ["Счет 64686473678894779589", "Счет 73654108430135874305"]


# Тест нормальных вводных
@pytest.mark.parametrize("input_text, card_or_account, counter", [("Maestro 1596837868705199", "card", 16),
                                                                  ("Счет 64686473678894779589", "account", 20),
                                                                  ("MasterCard 7158300734726758", "card", 16),
                                                                  ("Счет 35383033474447895560", "account", 20),
                                                                  ("Visa Classic 6831982476737658", "card", 16),
                                                                  ("Visa Platinum 8990922113665229", "card", 16),
                                                                  ("Visa Gold 5999414228426353", "card", 16),
                                                                  ("Счет 73654108430135874305", "account", 20)
                                                                  ])
def test_account_or_card(input_text, card_or_account, counter):
    assert account_or_card(input_text)[0] == card_or_account
    assert account_or_card(input_text)[1] == counter

# Тест ввода карты с ошибкой
def test_account_or_card_err_card():
    with pytest.raises(ValueError) as err_card:
        account_or_card("1596837868705199")
    with pytest.raises(ValueError) as err_card:
        account_or_card(" 1596837868705199")
    assert str(err_card.value) == "Пожалуйста, укажите название карты в начале"

# Тест ввода счета с ошибкой
def test_account_or_card_err_acc():
    with pytest.raises(ValueError) as err_acc:
        account_or_card("Счт 73654108430135874305")
    with pytest.raises(ValueError) as err_acc:
        account_or_card("73654108430135874305")
    assert str(err_acc.value) == "Пожалуйста, укажите слово __Счет__ в начале"

# Тест ввода номера карты или счета с ошибкой
def test_account_or_card_err_numbers():
    with pytest.raises(ValueError) as no_num:
        account_or_card("Счет 123456789012345678901")
    assert str(no_num.value) == "Введено неверное количество цифр. 16 - для карты и 20 - для счета"

# Тест итоговый маскировки карты
def test_mask_account_card(user_text_card):
    assert mask_account_card(user_text_card[0]) == "Maestro 1596 83** **** 5199"
    assert mask_account_card(user_text_card[1]) == "Visa Classic 6831 98** **** 7658"

# Тест итоговый маскировки счета
def test_mask_account_acc(user_text_acc):
    assert mask_account_card(user_text_acc[0]) == "Счет **9589"
    assert mask_account_card(user_text_acc[1]) == "Счет **4305"

# Тест форматирования даты при нормальном вводе
def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("0000-01-01") == "01.01.0000"
    assert get_date("9999-12-31") == "31.12.9999"

# Тест форматирования даты при вводе с ошибкой
def test_get_date_no_date():
    with pytest.raises(ValueError) as no_date:
        get_date("1234-q12-331")
    with pytest.raises(ValueError) as no_date:
        get_date("000-10-10")
    assert str(no_date.value) == "Проверьте формат и значение вводимых данных"

    with pytest.raises(ValueError) as err_date:
        get_date("2920-13-09")
    with pytest.raises(ValueError) as err_date:
        get_date("0000-12-32")
    with pytest.raises(ValueError) as err_date:
        get_date("0000-00-31")
    assert str(err_date.value) == "Указаны неверные значения даты"
