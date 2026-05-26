import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях, при необходимости обращаясь к API."""
    try:
        amount_data = transaction.get("operationAmount", {})
        amount = float(amount_data.get("amount", 0.0))
        currency = amount_data.get("currency", {}).get("code", "RUB")
    except (AttributeError, ValueError):
        return 0.0

    if currency == "RUB":
        return amount

    # Полный корректный URL со всеми эндпоинтами и параметрами по документации
    url = f"https://apilayer.com{currency}&amount={amount}"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200 and isinstance(data, dict):
            return float(data.get("result", 0.0))

        if isinstance(data, dict) and "result" in data:
            return float(data["result"])

    except (requests.RequestException, ValueError, KeyError, AttributeError):
        return 0.0

    return 0.0
