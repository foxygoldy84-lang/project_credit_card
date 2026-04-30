# Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску.
# Номер карты замаскирован и отображается в формате XXXX XX** **** XXXX, где X — это цифра номера.
# То есть видны первые 6 цифр и последние 4 цифры, остальные символы отображаются звездочками, номер разбит по блокам по 4 цифры, разделенным пробелами. Пример работы функции:
# 7000792289606361 входной аргумент
# 7000 79** **** 6361 выход функции

from black.nodes import Union


def get_mask_card_number(card_number: Union[int]) -> Union[str]:
    """Функция маскировки номера банковской карты"""
    card_str = str(card_number)
    first_four = card_str[0:4]
    four_six = card_str[4:6]
    last_four = card_str[-4:]

    if len(card_str) != 16:
        return "Количество цифр должно быть 16"
    result = f"{first_four} {four_six}** **** {last_four}"
    return result


print(get_mask_card_number(1234567819584775))


# Функция get_mask_account принимает на вход номер счета и возвращает его маску.
# Номер счета замаскирован и отображается в формате **XXXX, где X — это цифра номера.
# То есть видны только последние 4 цифры номера, а перед ними — две звездочки. Пример работы функции:
# 73654108430135874305 входной аргумент
# **4305 выход функции


def get_mask_account(number_core: Union[int]) -> Union[str]:
    """Функция маскировки номера банковского счета"""
    card_str = str(number_core)
    if len(card_str) != 20:
        return "Количество цифр должно быть 20"
    last_four = card_str[-4:]
    mask_card_str = "**" + last_four
    return mask_card_str


print(get_mask_account(12345678987654321345))
