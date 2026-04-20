def filter_by_state(data, state='EXECUTED') -> str:
"""Функция  возвращает новый список по ключу 'state'"""
new_state = []
for i in data:
    if i.get('state') == 'state':
        new_state.append(i)

return new_state