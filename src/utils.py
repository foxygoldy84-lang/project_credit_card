import json
import os
from typing import Any, Dict, List


def list_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл и возвращает список транзакций."""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        return []
