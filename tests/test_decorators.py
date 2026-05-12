from ctypes import pydll
from fileinput import filename

import pytest
import os
from src.decorators import log

# Тест 1: Успешное выполнение и вывод в консоль
def test_log_console_ok(capsys):
    @log()
    def my_function(x, y):
        return x + y

    my_function(1, 2)
    captured = capsys.readouterr()
    assert "my_function ok" in captured.out

# Тест 2: Щшибка и вывод в консоль
def test_log_console_error(capsys):
    @log()
    def my_function(x, y):
        return x / 0

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    captured = capsys.readouterr()
    assert "my_function error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out

#Тест 3: Запись в файл при успешном выполнении
def test_log_file_ok():
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    @log(filename=filename)
    def my_function(x, y):
        return x + y

    my_function(1, 2)

    with open(filename, "r") as f:
        log_content = f.read()

    assert  "my_function ok" in log_content
    os.remove(filename)


# Тест 4: Запись в файл при ошибке
def test_log_file_error():
    filename = "test_error_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    @log(filename=filename)
    def my_function(x, y):
        raise ValueError("test error")

    with pytest.raises(ValueError):
        my_function(1, 2)

    with open(filename, "r") as f:
        log_content = f.read()

    assert "my_function error: ValueError. Inputs: (1, 2), {}" in log_content
    os.remove(filename)

