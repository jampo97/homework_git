from masks import get_mask_card_number
from masks import get_mask_account


def mask_account_card(user_input: str) -> str:
    """функция маскировки введенных данных (счета или номера карты)"""

    masked_account_card: str = ""
    card_or_account: str = account_or_card(user_input)[0]   # результат проверки - карта/счет
    count_numbers = int(account_or_card(user_input)[1])     # количество цифр в вводе пользователя

    if card_or_account == "card":
        user_input_card_number = user_input[-count_numbers:]
        masked_number = get_mask_card_number(user_input_card_number)
        masked_account_card = user_input[:-count_numbers] + masked_number

    if card_or_account == "account":
        user_input_account_number = user_input[-count_numbers:]
        masked_number = get_mask_account(user_input_account_number)
        masked_account_card = user_input[:-count_numbers] + masked_number



    return masked_account_card


def account_or_card(user_input: str) -> list[str]:
    """функция определяющая что введено - карта или счет и подсчет цифр в вводе"""

    card_or_account: str = "error"
    counter: int = 0
    count_num_in_account: int = 20
    count_num_in_card: int = 16

    for item in user_input:  # счетчик количества цифр в вводе
        if item.isnumeric():
            counter += 1

    if counter == count_num_in_card:  # 1 условие проверки для карты
        card_or_account = "card"
    elif counter == count_num_in_account and "Счет" in user_input:  # 2 условия проверки для счета
        card_or_account = "account"

    else:
        card_or_account = "error"

    return [card_or_account, counter]



inputs: list[str] = ["Maestro 1596837868705199", "Счет 64686473678894779589", "MasterCard 7158300734726758",
          "Счет 35383033474447895560", "Visa Classic 6831982476737658", "Visa Platinum 8990922113665229",
          "Visa Gold 5999414228426353", "Счет 73654108430135874305"]
for item in inputs:
    print (mask_account_card(item))