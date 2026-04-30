import pytest
from generators.filter_by_currency import filter_by_currency, transaction_descriptions, card_number_generator

# Фикстура с тестовыми данными транзакций (название БЕЗ test_)
@pytest.fixture
def transactions_data():
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод со счета на счет"},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Оплата услуг"},
        {"id": 4, "description": "Без валюты"}
    ]

# Тест для filter_by_currency
@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 2),
    ("RUB", 1),
    ("EUR", 0)
])
def test_filter_by_currency(transactions_data, currency, expected_count):
    """Проверка фильтрации по разным валютам."""
    result = list(filter_by_currency(transactions_data, currency))
    assert len(result) == expected_count




