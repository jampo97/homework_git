from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(user_input: str) -> str:
    """Функция маскировки введенных данных (счета или номера карты)"""

    masked_account_card: str = ""
    card_or_account: str = account_or_card(user_input)[0]  # результат проверки - карта/счет
    count_numbers: int = account_or_card(user_input)[1]  # количество цифр во вводе пользователя

    if card_or_account == "card":
        user_input_card_number = user_input[-count_numbers:]
        masked_number = get_mask_card_number(user_input_card_number)
        masked_account_card = user_input[:-count_numbers] + masked_number

    if card_or_account == "account":
        user_input_account = user_input[-count_numbers:]
        masked_number = get_mask_account(user_input_account)
        masked_account_card = user_input[:-count_numbers] + masked_number

    return masked_account_card


def account_or_card(user_input: str) -> list:
    """Функция определяющая, что введено - карта или счет и подсчет цифр во вводе"""

    card_or_account: str = ""
    counter: int = 0
    count_num_in_account: int = 20
    count_num_in_card: int = 16

    for item in user_input:  # счетчик количества цифр во вводе
        if item.isnumeric():
            counter += 1

    if counter == count_num_in_account:  # 1 условие проверки для корректного ввода номера счета
        card_or_account = "account"
        if "Счет" not in user_input:  # 2 условие проверки для ввода слова "Счет"
            raise ValueError("Пожалуйста, укажите слово __Счет__ в начале")

    elif counter == count_num_in_card:  # 1 условие проверки для корректного ввода номера карты
        card_or_account = "card"
        if not user_input[0].isalpha() or user_input[0].isdigit():  # 2 условие проверки для ввода названия карты
            raise ValueError("Пожалуйста, укажите название карты в начале")

    elif counter != count_num_in_account and counter != count_num_in_card:
        raise ValueError(f"Введено неверное количество цифр. "
                         f"{count_num_in_card} - для карты и "
                         f"{count_num_in_account} - для счета")

    return [card_or_account, counter]


def get_date(input_date: str) -> str:
    """Форматирование данных о дате в формат ДД.ММ.ГГГГ"""

    date_format: str = ""
    year: str = input_date[0:4]
    month: str = input_date[5:7]
    day: str = input_date[8:10]

    if not year.isdigit() or not month.isdigit() or not day.isdigit():
        raise ValueError("Проверьте формат и значение вводимых данных")

    elif int(month) > 12 or int(month) < 1 or int(day) > 31 or int(day) < 1:
        raise ValueError("Указаны неверные значения даты")

    date_format = f"{day}.{month}.{year}"

    return date_format


inputs: list[str] = [
    "Maestro 1596837868705199",
    "Счет 64686473678894779589",
    "MasterCard 7158300734726758",
    "Счет 35383033474447895560",
    "Visa Classic 6831982476737658",
    "Visa Platinum 8990922113665229",
    "Visa Gold 5999414228426353",
    "Счет 73654108430135874305",
]
for item in inputs:
    print(mask_account_card(item))
print(get_date("2024-03-11T02:26:18.671407"))
