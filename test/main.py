def filter_by_state(data, state='EXECUTED') -> str:
"""Функция  возвращает новый список по ключу 'state'"""
new_state = []
for i in data:
    if i.get('state') == 'state':
        new_state.append(i)

return new_state



def sort_by_date(data, reverse=True):
    """Функция сортирует список словарей по ключу 'date'"""
    sorted_data = sorted(data, key=lambda x: x['date'], reverse=reverse)
    return sorted_data