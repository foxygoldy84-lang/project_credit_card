from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


@pytest.fixture
def rub_transaction():
    """Фикстура для транзакции в рублях."""
    return {"operationAmount": {"amount": "150.50", "currency": {"code": "RUB"}}}


@pytest.fixture
def usd_transaction():
    """Фикстура для транзакции в долларах."""
    return {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}


def test_convert_rub(rub_transaction):
    """Тест конвертации рублей без вызова API."""
    assert convert_to_rub(rub_transaction) == 150.50


@patch("src.external_api.requests.get")
def test_convert_usd_success(mock_get, usd_transaction):
    """Тест успешного ответа от API при конвертации USD."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.0}
    mock_get.return_value = mock_response

    assert convert_to_rub(usd_transaction) == 7500.0


@patch("src.external_api.requests.get")
def test_convert_usd_api_failure(mock_get, usd_transaction):
    """Тест поведения функции при ошибке внешнего API."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    assert convert_to_rub(usd_transaction) == 0.0

