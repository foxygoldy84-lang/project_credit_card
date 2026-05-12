from ctypes import pydll

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

#Тест 3:

