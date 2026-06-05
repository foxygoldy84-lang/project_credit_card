import os
from typing import Any, Dict, List, Optional, Union

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import list_transactions, read_transactions_csv, read_transactions_xlsx


def mask_payment_info(payment_info: Optional[Union[str, int]]) -> str:
    """Вспомогательная функция для маскирования строк типа 'Счет 1234...' или 'Visa 1234...'"""
    if not payment_info or payment_info is None:
        return ""

    # Преобразуем в строку на случай, если пришел отличный от str тип данных
    payment_info_str: str = str(payment_info).strip()

    if payment_info_str.lower().startswith("счет"):
        try:
            name, number = payment_info_str.split(maxsplit=1)
            return f"{name} {get_mask_account(number)}"
        except ValueError:
            return payment_info_str
    else:
        try:
            parts: List[str] = payment_info_str.split()
            number: str = parts[-1]
            name: str = " ".join(parts[:-1])
            return f"{name} {get_mask_card_number(number)}"
        except ValueError:
            return payment_info_str


def main() -> None:
    # Путь к папке с файлами данных (data) относительно корня проекта
    data_dir: str = os.path.join(os.path.dirname(__file__), "..", "data")

    # Переменная для хранения итогового списка транзакций
    transactions: List[Dict[str, Any]] = []

    # 1. Приветствие и выбор файла данных
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        file_choice: str = input("\nПользователь: ").strip()
        if file_choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            transactions = list_transactions(os.path.join(data_dir, "operations.json"))
            break
        elif file_choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            transactions = read_transactions_csv(os.path.join(data_dir, "transactions.csv"))
            break
        elif file_choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            transactions = read_transactions_xlsx(os.path.join(data_dir, "transactions_excel.xlsx"))
            break
        else:
            print("Неверный пункт меню. Пожалуйста, выберите 1, 2 или 3.")

    # 2. Выбор и валидация статуса операции через цикл
    valid_statuses: List[str] = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        status_input: str = input("\nПользователь: ").strip().upper()

        if status_input in valid_statuses:
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            transactions = filter_by_state(transactions, status_input)
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # 3. Запрос на сортировку по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    date_sort_choice: str = input("\nПользователь: ").strip().lower()

    if date_sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        sort_order: str = input("\nПользователь: ").strip().lower()

        if "возраст" in sort_order:
            transactions = sort_by_date(transactions, reverse=False)
        else:
            transactions = sort_by_date(transactions, reverse=True)

    # 4. Фильтрация по валюте (благодаря вашим функциям структура теперь одинаковая)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice: str = input("\nПользователь: ").strip().lower()
    if rub_choice == "да":
        transactions = [
            tx for tx in transactions if tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # 5. Фильтрация по поисковому слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    desc_choice: str = input("\nПользователь: ").strip().lower()
    if desc_choice == "да":
        search_word: str = input("\nВведите слово для поиска: ").strip().lower()
        transactions = [tx for tx in transactions if search_word in str(tx.get("description", "")).lower()]

    # 6. Вывод итоговых результатов в консоль
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Программа: Всего банковских операций в выборке: {len(transactions)}\n")

        for tx in transactions:
            # Превращаем дату из ISO формата (2019-12-08...) в формат DD.MM.YYYY
            date_str: Any = tx.get("date", "")
            date_formatted: str = "Дата неизвестна"
            if date_str and len(str(date_str)) >= 10:
                date_str_clean: str = str(date_str)
                date_formatted = f"{date_str_clean[8:10]}.{date_str_clean[5:7]}.{date_str_clean[0:4]}"

            description: str = str(tx.get("description", "Перевод"))

            # Маскируем отправителя и получателя с помощью ваших функций из masks.py
            from_info: Any = tx.get("from")
            to_info: Any = tx.get("to")

            from_masked: str = mask_payment_info(from_info)
            to_masked: str = mask_payment_info(to_info)

            transfer_route: str = ""
            if from_masked:
                transfer_route = f"{from_masked} -> {to_masked}"
            else:
                transfer_route = to_masked

            # Извлекаем сумму и наименование валюты
            amount_data: Dict[str, Any] = tx.get("operationAmount", {})
            amount: Any = amount_data.get("amount", "0")
            currency: str = amount_data.get("currency", {}).get("name", "руб.")

            if currency == "RUB":
                currency = "руб."

            # Итоговый вывод блока одной транзакции
            print(f"{date_formatted} {description}")
            if transfer_route:
                print(transfer_route)
            print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
