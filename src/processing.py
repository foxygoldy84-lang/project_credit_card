def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращает новый список по ключу 'state'"""
    new_state = []
    for item in data:
        if item.get("state") == state:
            new_state.append(item)

    return new_state


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Функция сортирует список словарей по ключу 'date'"""
    sorted_data = sorted(data, key=lambda x: x["date"], reverse=reverse)
    return sorted_data
