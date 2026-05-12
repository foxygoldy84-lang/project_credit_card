import os
from typing import Any

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


# Тест 1: Успешное выполнение и вывод в консоль
def test_log_console_ok(capsys: CaptureFixture) -> None:
    @log()
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, 2)
    captured = capsys.readouterr()
    assert "my_function ok" in captured.out


# Тест 2: Ошибка и вывод в консоль
def test_log_console_error(capsys: CaptureFixture) -> None:
    @log()
    def my_function(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    captured = capsys.readouterr()
    assert "my_function error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


# Тест 3: Запись в файл при успешном выполнении
def test_log_file_ok() -> None:
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    @log(filename=filename)
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, 2)

    with open(filename, "r") as f:
        log_content = f.read()

    assert "my_function ok" in log_content
    os.remove(filename)


# Тест 4: Запись в файл при ошибке
def test_log_file_error() -> None:
    filename = "test_error_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    @log(filename=filename)
    def my_function(x: int, y: int) -> Any:
        raise ValueError("test error")

    with pytest.raises(ValueError):
        my_function(1, 2)

    with open(filename, "r") as f:
        log_content = f.read()

    assert "my_function error: ValueError. Inputs: (1, 2), {}" in log_content
    os.remove(filename)
