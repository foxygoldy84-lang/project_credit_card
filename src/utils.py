import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd

# Создаем папку logs в корне проекта, если её ещё нет
os.makedirs("logs", exist_ok=True)

# Настройка логера для модуля utils
logger = logging.getLogger("utils")
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def list_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл и возвращает список транзакций."""
    logger.info(f"Запрос на чтение транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден по пути: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Файл успешно прочитан. Найдено транзакций: {len(data)}")
                return data
            logger.warning(f"Данные в файле {file_path} не являются списком")
            return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка чтения файла {file_path}: неверный формат JSON")
        return []


def read_transactions_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и приводит к стандартному виду."""
    logger.info(f"Запрос на чтение транзакций из CSV-файла: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"CSV-файл не найден по пути: {file_path}")
        return []

    try:
        # Читаем CSV с разделителем точка с запятой
        df = pd.read_csv(file_path, sep=";")

        # Заменяем пустые значения (NaN) на None для совместимости с JSON структурой
        df = df.astype(object).where(pd.notnull(df), None)

        transactions = []
        for _, row in df.iterrows():
            transaction = {
                "id": row.get("id"),
                "state": row.get("state"),
                "date": row.get("date"),
                "operationAmount": {
                    "amount": row.get("amount"),
                    "currency": {"name": row.get("currency_name"), "code": row.get("currency_code")},
                },
                "from": row.get("from"),
                "to": row.get("to"),
                "description": row.get("description"),
            }
            transactions.append(transaction)

        logger.info(f"CSV-файл успешно прочитан. Найдено транзакций: {len(transactions)}")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения CSV-файла {file_path}: {e}")
        return []


def read_transactions_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из XLSX-файла и приводит к стандартному виду."""
    logger.info(f"Запрос на чтение транзакций из Excel-файла: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"Excel-файл не найден по пути: {file_path}")
        return []

    try:
        # Читаем Excel таблицу
        df = pd.read_excel(file_path)

        # Заменяем пустые значения (NaN) на None
        df = df.astype(object).where(pd.notnull(df), None)

        transactions = []
        for _, row in df.iterrows():
            transaction = {
                "id": row.get("id"),
                "state": row.get("state"),
                "date": row.get("date"),
                "operationAmount": {
                    "amount": row.get("amount"),
                    "currency": {"name": row.get("currency_name"), "code": row.get("currency_code")},
                },
                "from": row.get("from"),
                "to": row.get("to"),
                "description": row.get("description"),
            }
            transactions.append(transaction)

        logger.info(f"Excel-файл успешно прочитан. Найдено транзакций: {len(transactions)}")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения Excel-файла {file_path}: {e}")
        return []
