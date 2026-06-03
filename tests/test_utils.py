import json
from unittest.mock import mock_open, patch

import pandas as pd  # noqa: F401
import pytest

from src.utils import (
    list_transactions,
    process_bank_operations,
    process_bank_search,
    read_transactions_csv,
    read_transactions_xlsx,
)


def test_list_transactions_success() -> None:
    mock_data = json.dumps([{"id": 1, "amount": 100}])
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            assert list_transactions("dummy.json") == [{"id": 1, "amount": 100}]


def test_list_transactions_file_not_found() -> None:
    with patch("os.path.exists", return_value=False):
        assert list_transactions("dummy.json") == []


def test_list_transactions_invalid_json() -> None:
    with patch("builtins.open", mock_open(read_data="not json")):
        with patch("os.path.exists", return_value=True):
            assert list_transactions("dummy.json") == []


def test_list_transactions_not_a_list() -> None:
    mock_data = json.dumps({"id": 1})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            assert list_transactions("dummy.json") == []


@pytest.fixture
def mock_df_data() -> pd.DataFrame:
    """Фикстура, возвращающая DataFrame с тестовыми данными."""
    return pd.DataFrame(
        [
            {
                "id": 650703,
                "state": "EXECUTED",
                "date": "2023-09-05",
                "amount": 16210.0,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            }
        ]
    )


def test_read_transactions_csv_success(mock_df_data: pd.DataFrame) -> None:
    """Тест успешного чтения CSV-файла через патч pandas."""
    with patch("os.path.exists", return_value=True):
        with patch("pandas.read_csv", return_value=mock_df_data):
            result = read_transactions_csv("dummy.csv")

            assert len(result) == 1
            assert result[0]["id"] == 650703
            assert result[0]["operationAmount"]["amount"] == 16210.0
            assert result[0]["operationAmount"]["currency"]["code"] == "PEN"


def test_read_transactions_csv_file_not_found() -> None:
    """Тест возврата пустого списка, если CSV-файл не существует."""
    with patch("os.path.exists", return_value=False):
        assert read_transactions_csv("dummy.csv") == []


def test_read_transactions_csv_error() -> None:
    """Тест возврата пустого списка при ошибке чтения CSV (например, поврежденный файл)."""
    with patch("os.path.exists", return_value=True):
        with patch("pandas.read_csv", side_effect=Exception("Ошибка чтения")):
            assert read_transactions_csv("dummy.csv") == []


def test_read_transactions_xlsx_success(mock_df_data: pd.DataFrame) -> None:
    """Тест успешного чтения Excel-файла через патч pandas."""
    with patch("os.path.exists", return_value=True):
        with patch("pandas.read_excel", return_value=mock_df_data):
            result = read_transactions_xlsx("dummy.xlsx")

            assert len(result) == 1
            assert result[0]["state"] == "EXECUTED"
            assert result[0]["operationAmount"]["currency"]["name"] == "Sol"


def test_read_transactions_xlsx_file_not_found() -> None:
    """Тест возврата пустого списка, если Excel-файл не существует."""
    with patch("os.path.exists", return_value=False):
        assert read_transactions_xlsx("dummy.xlsx") == []


def test_read_transactions_xlsx_error() -> None:
    """Тест возврата пустого списка при ошибке чтения Excel."""
    with patch("os.path.exists", return_value=True):
        with patch("pandas.read_excel", side_effect=Exception("Ошибка чтения")):
            assert read_transactions_xlsx("dummy.xlsx") == []


def test_process_bank_search():
    mock_data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата мобильной связи"},
        {"id": 3, "description": "Перевод другу"},
        {"id": 4, "description": ""},
    ]

    result = process_bank_search(mock_data, "перевод")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_empty_or_no_match():
    mock_data = [{"id": 1, "description": "Покупка продуктов"}]

    assert process_bank_search(mock_data, "Кредит") == []
    assert process_bank_search([], "Покупка") == []


def test_process_bank_operations():
    mock_data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата мобильной связи"},
        {"id": 3, "description": "Перевод другу"},
        {"id": 4, "description": "Покупка продуктов"},
    ]
    categories = ["Перевод", "Оплата", "Кредит"]

    result = process_bank_operations(mock_data, categories)

    assert result == {"Перевод": 2, "Оплата": 1, "Кредит": 0}
