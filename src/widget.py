from datetime import datetime
from src.masks import get_mask_card_number, get_mask_account



def mask_account_card(data: str) -> str:
    """Маскирует данные карты или счета."""
    parts = data.split()
    number = parts[-1]
    name = " ".join(parts[:-1])
    if "Счет" in name:
        masked_number = get_mask_account(int(number))
    else:
        masked_number = get_mask_card_number(int(number))
    return f"{name.title()} {masked_number}"



def get_date(data_string: str) -> str:
    """Преобразует строку с датой в формат дд.мм.гггг"""
    try:
        data_iso = data_string[:10]
        date_obj = datetime.strptime(data_iso, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return "Ошибка: некорректный формат даты."



if __name__ == "__main__":
    print(mask_account_card("visa platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))

