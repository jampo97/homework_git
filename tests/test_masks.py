import pytest
from src.masks import get_mask_card_number, get_mask_account

# Тест маскировки номера карты при нормальном вводе
@pytest.mark.parametrize("input_card, output_card", [("7158300734726758", "7158 30** **** 6758"),
                                                     ("1234560000001234", "1234 56** **** 1234")])
def test_get_mask_card_number(input_card, output_card):
    assert get_mask_card_number(input_card) == output_card

# Тест маскировки номера счета при нормальном вводе
@pytest.mark.parametrize("input_account, output_account", [("35383033474447895560", "**5560"),
                                                           ("73654108430135874305", "**4305")])
def test_get_mask_account(input_account, output_account):
    assert get_mask_account(input_account) == output_account
