import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-11T22:46:18.988530"},
        {"id": 93979522, "state": "CANCELED", "date": "2018-06-16T04:10:25.795040"},
        {"id": 59422340, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
        {"id": 14223965, "state": "PENDING", "date": "2021-12-01T12:00:00.000000"}
    ]
