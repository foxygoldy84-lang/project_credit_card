import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Фикстура с тестовыми данными транзакций (название БЕЗ test_)


@pytest.fixture
def transactions_data():
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод со счета на счет"},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Оплата услуг"},
        {"id": 4, "description": "Перевод юр. лицам"},
        {"id": 5, "description": "Перевод физ. лицам"},
        {"id": 6, "description": "Зарплата"},
        {"id": 7, "description": "Без описания"}
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


def test_transaction_descriptions(transactions_data):
    """ Проверка получения описания банковский операций"""
    descriptions = list(transaction_descriptions(transactions_data))
    expected = ["Перевод организации", "Перевод со счета на счет", "Оплата услуг",
                "Перевод юр. лицам", "Перевод физ. лицам", "Зарплата", "Без описания"]
    assert descriptions == expected


def test_card_number_generator():
    """ Проверка генерации номеров карт и их формат выпуска. """
    gen = card_number_generator(1, 5)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"
    assert next(gen) == "0000 0000 0000 0004"
    assert next(gen) == "0000 0000 0000 0005"

    with pytest.raises(StopIteration):
        next(gen)
