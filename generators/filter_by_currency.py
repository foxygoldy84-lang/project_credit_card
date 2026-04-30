from typing import Iterable, List, Dict, Any


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterable[Dict[str, Any]]:
    """Генератор, который принимает список словарей с транзакциями и выдает с заданной валютой."""
    for transaction in transactions:
        # Извлекаем код валюты
        current_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

        if current_currency != currency:
            continue

        yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterable[str]:
    """Генератор, который принимает список словарей с транзакциями и возвращает описание каждой."""
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Iterable[str]:
    """Генератор, который создает номера карт в заданном формате."""
    for number in range(start, end + 1):
        number_str = f"{number:016}"
        formatted_card = f"{number_str[:4]} {number_str[4:8]} {number_str[8:12]} {number_str[12:16]}"
        yield formatted_card

