# Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску.
# Номер карты замаскирован и отображается в формате XXXX XX** **** XXXX, где X — это цифра номера.
# То есть видны первые 6 цифр и последние 4 цифры, остальные символы отображаются звездочками,
# номер разбит по блокам по 4 цифры, разделенным пробелами.
# Пример работы функции:
# 7000792289606361 входной аргумент
# 7000 79** **** 6361 выход функции
import logging
import os
from typing import Union

# Создаем папку logs в корне проекта, если её ещё нет
os.makedirs("logs", exist_ok=True)

# Настройка логера для модуля masks
logger = logging.getLogger("masks")
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Функция маскировки номера банковской карты"""
    logger.info("Начало маскирования номера карты.")
    card_str = str(card_number)

    if len(card_str) != 16:
        logger.error(f"Ошибка маскирования карты. Неверная длина: {len(card_str)} символов.")
        return "Количество цифр должно быть 16"

    first_four = card_str[0:4]
    four_six = card_str[4:6]
    last_four = card_str[-4:]

    result = f"{first_four} {four_six}** **** {last_four}"
    logger.info("Номер карты успешно замаскирован.")
    return result


def get_mask_account(number_core: Union[int, str]) -> str:
    """Функция маскировки номера банковского счета"""
    logger.info("Начало маскирования номера счета.")
    card_str = str(number_core)

    if len(card_str) != 20:
        logger.error(f"Ошибка маскирования счета. Неверная длина: {len(card_str)} символов.")
        return "Количество цифр должно быть 20"

    last_four = card_str[-4:]
    mask_card_str = "**" + last_four
    logger.info("Номер счета успешно замаскирован.")
    return mask_card_str


# Тестовые принты (при запуске модуля создадут записи в файле logs/masks.log)
if __name__ == "__main__":
    print(get_mask_card_number(1234567819584775))
    print(get_mask_account(12345678987654321345))
