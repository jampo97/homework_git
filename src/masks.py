import logging
import os

my_logger = logging.getLogger("masks")
my_logger.setLevel(logging.INFO)
log_filename = os.path.join(os.path.dirname(__file__), "..", "logs", "masks.log")
file_handler = logging.FileHandler(log_filename, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)


def get_mask_card_number(user_input_card_number: str) -> str:
    """Функция маскировки номера банковской карты"""

    counter: int = 0
    masked_card_number: str = ""
    len_card = len(user_input_card_number)
    start_num = 6  # количество цифр, отображаемых в начале
    end_num = 4  # количество цифр, отображаемых в конце
    my_logger.info("Старт функции get_mask_card_number/ получено корректное значение")
    try:
        int(user_input_card_number)
    except ValueError:
        raise ValueError("Введены лишние символы. нужно только номер карты")

    for num in user_input_card_number:

        if counter > 3 and counter % 4 == 0:  # ставим разделитель через 4 знака
            masked_card_number += " "

        counter += 1

        if counter < start_num + 1:  # показываем первые цифры
            masked_card_number += num
            continue

        if counter > (len_card - end_num):  # показываем последние цифры
            masked_card_number += num
            continue

        masked_card_number += "*"  # остальные не показываем
    my_logger.info(f"Получен замаскированный номер карты {masked_card_number}")
    return masked_card_number


def get_mask_account(user_input_account: str) -> str:
    """Функция маскировки номера банковского счетa"""

    counter: int = 0
    masked_account: str = "**"
    len_account = len(user_input_account)
    end_num = 4  # количество цифр, отображаемых в конце
    my_logger.info("Старт функции get_mask_account/ получено корректное значение")
    try:
        int(user_input_account)
    except ValueError:
        raise ValueError("Введены лишние символы. нужно только номер счета")

    for num in user_input_account:

        counter += 1

        if counter > (len_account - end_num):  # показываем последние цифры
            masked_account += num
            continue
    my_logger.info(f"Получен замаскированный номер счета {masked_account}")
    return masked_account
