import pytest
from src.masks import get_mask_card_number

@pytest.mark.parametrize("card_num, expected", [
    (1234567812345678, "1234 56** **** 5678"),
    (12345, "Количество цифр должно быть 16")
])
def test_get_mask_card_number(card_num, expected):
    """Тестируем маскировку номера карты"""
    assert get_mask_card_number(card_num) == expected






