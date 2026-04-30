import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize("input_data, expected",[("Visa Platinum 1234567890587685", "Visa Platinum 1234 56** **** 7685"),
                                                   ("Maestro 1234567890587685", "Maestro 1234 56** **** 7685"),
                                                   ("Счет 12345687657890587685", "Счет **7685")])
def test_mask_account_card(input_data, expected):
    """ Тестируем корректный вывод маски карты. """
    assert mask_account_card(input_data) == expected

@pytest.mark.parametrize("date_str, expected", [
    ("2026-03-11T02:26:18.671407", "11.03.2026"),
    ("2014-12-31T14:00:00", "31.12.2014"),
    ("некорректная дата", "Ошибка: некорректный формат даты.")])

def test_get_date(date_str, expected):
    """ Тестируем на вывод даты в формате ДД.ММ.ГГГГ """
    assert get_date(date_str) == expected


