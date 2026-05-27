import json
import logging
import os
from typing import Any, Dict, List

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
