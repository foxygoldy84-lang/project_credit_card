import json
from unittest.mock import mock_open, patch
from src.utils import list_transactions


def test_list_transactions_success():
    mock_data = json.dumps([{"id": 1, "amount": 100}])
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            assert list_transactions("dummy.json") == [{"id": 1, "amount": 100}]


def test_list_transactions_file_not_found():
    with patch("os.path.exists", return_value=False):
        assert list_transactions("dummy.json") == []


def test_list_transactions_invalid_json():
    with patch("builtins.open", mock_open(read_data="not json")):
        with patch("os.path.exists", return_value=True):
            assert list_transactions("dummy.json") == []


def test_list_transactions_not_a_list():
    mock_data = json.dumps({"id": 1})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            assert list_transactions("dummy.json") == []
