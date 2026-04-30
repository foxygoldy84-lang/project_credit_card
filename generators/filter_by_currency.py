from typing import Iterable, list, Dict, Any

def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) ->  Iterable[Dikt[str, Any]]:
    """ Генератор, который принимает список словарей с транзакцией и выдает с заданной валютой"""
    for  transaction in transactions:
        current_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if current_currency != currency:
            continue

        yield transaction

