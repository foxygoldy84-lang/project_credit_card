from src.processing import sort_by_date, filter_by_state

def test_sort_by_date_missing_date():
    """ Тестируем транзакции на отсутствие даты. """
    data = [
        {"id": 1, "date": "2023-01-01T12:00:00"},
        {"id": 2,},
        {"id": 3, "date": "2024-01-01T12:00:00"}
    ]

    result = sort_by_date(data, reverse=True)
    assert len(result) == 3

def test_filter_by_state(sample_transactions):
    """ Тестируем фильтрацию (данные прилетают из conftest.py) """
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 2
