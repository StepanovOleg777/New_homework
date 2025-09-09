import pytest
import sys
from io import StringIO
from unittest.mock import patch


def test_main_execution():
    """Тест что main.py выполняется без ошибок"""
    try:
        from main import main

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            result = main()

        # Проверяем что программа завершилась успешно
        assert result == 0

        # Проверяем что в выводе есть ожидаемый текст
        output = mock_stdout.getvalue()
        assert "ТЕСТИРОВАНИЕ ПРОГРАММЫ" in output
        assert "ВСЕ ТЕСТЫ ПРОЙДЕНЫ" in output
        assert "Средний ценник" in output

    except Exception as e:
        pytest.fail(f"Main execution failed: {e}")


def test_main_zero_quantity_error():
    """Тест обработки ошибки нулевого количества в main"""
    from main import main

    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        result = main()
        output = mock_stdout.getvalue()

        # Проверяем что ошибка нулевого количества обработана
        assert "Возникла ошибка ValueError" in output
        assert "нулевым количеством" in output
