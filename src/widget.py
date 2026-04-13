from datetime import datetime

from black.nodes import Union


def mask_account_card(data: str) -> str:
    """Функция маскировки карты и счета"""
    parts = data.split()
    name = " ".join(parts[:-1])
    number = parts[-1]

    if not number.isdigit():
        return "Ошибка, номер должен состоять только из цифр"

    if name.lower().startswith("счет"):
        if len(number) != 20:
            return "Номер сета должен содержать 20 цифр"
        masked_number = f"**{number[-4:]}"
    else:
        if len(number) != 16:
            return "Номер карты должен содержать 16 цифр"
        masked_number = f"**{number[:4] {number[4:6]}** **** {number[-4:]"
                
return f"{name.title()} {masked_number}"


def get_data(data_string: str) -> str:
    """Преобразует строку в формат дд.мм.гггг"""
    try:
        data_iso = data_string[:10]
        data_obj = datetime.strptime("%d.%m.%Y")
        return data_obj.strftime("%d.%m.%Y")
    except ValueError:
        return "Ошибка: некорректный ввод данных."






