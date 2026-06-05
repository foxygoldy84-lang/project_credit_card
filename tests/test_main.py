from src.main import main, mask_payment_info


# Тестируем функцию маскирования (вспомогательную)
def test_mask_payment_info_card():
    assert "Visa 1234 56** **** 3456" in mask_payment_info("Visa 1234567890123456")


def test_mask_payment_info_account():
    assert "Счет **4321" in mask_payment_info("Счет 12345678901234564321")


def test_mask_payment_info_empty():
    assert mask_payment_info("") == ""
    assert mask_payment_info(None) == ""


# Тестируем основную функцию main с помощью фикстур monkeypatch и capsys
def test_main_successful_flow(monkeypatch, capsys):
    # Имитируем ответы пользователя по шагам:
    # 1. Выбрать JSON-файл -> "1"
    # 2. Ввести статус операции -> "EXECUTED"
    # 3. Сортировать по дате? -> "да"
    # 4. По возрастанию или убыванию? -> "по убыванию"
    # 5. Только рублевые? -> "нет"
    # 6. Фильтровать по слову? -> "нет"
    inputs = ["1", "EXECUTED", "да", "по убыванию", "нет", "нет"]

    # Подменяем стандартный input() на наш список ответов
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    # Запускаем главную функцию проекта
    main()

    # Перехватываем всё, что функция напечатала в консоль (через print)
    captured = capsys.readouterr().out

    # Проверяем, что программа вывела нужные реплики
    assert "Для обработки выбран JSON-файл." in captured
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured
    assert "Распечатываю итоговый список транзакций..." in captured


def test_main_invalid_status_retry(monkeypatch, capsys):
    # Проверяем сценарий, когда пользователь сначала вводит неверный статус "test",
    # программа ругается и просит ввести заново, и затем пользователь вводит "CANCELED"
    inputs = ["1", "test", "CANCELED", "нет", "нет", "нет"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    main()

    captured = capsys.readouterr().out

    # Проверяем, что программа сообщила о недоступности статуса "TEST"
    assert 'Статус операции "TEST" недоступен.' in captured
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured


def test_main_empty_result(monkeypatch, capsys):
    # Проверяем случай, когда пользователь ищет слово, которого заведомо нет (например, "абвгде")
    # Из-за этого выборка станет пустой
    inputs = ["1", "EXECUTED", "нет", "нет", "да", "абвгде"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    main()

    captured = capsys.readouterr().out

    # Проверяем, что вывелось сообщение о пустой выборке
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in captured
