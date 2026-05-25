import os
import requests
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()
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

    if currency in ["USD", "EUR"]:
        url = f"https://apilayer.com{currency}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("result", 0.0))
        except requests.RequestException:
            pass

    return 0.0
