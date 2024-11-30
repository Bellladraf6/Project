#!/usr/bin/env python
"""Главный файл для управления проектом Django. Используется для выполнения административных задач, таких как миграции, запуск сервера разработки и выполнение команд."""

import os  # Модуль для работы с переменными окружения
import sys  # Модуль для работы с аргументами командной строки


def main():
    """
    Основная функция, которая задаёт настройки проекта и запускает необходимые команды.
    """
    # Устанавливаем переменную окружения для указания пути к настройкам проекта
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "project_management_system.settings"
    )
    try:
        # Импортируем метод для выполнения команд Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обрабатываем ошибку, если Django не установлен или не доступен
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Выполняем команду, переданную через терминал
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # Запускаем основную функцию, если файл выполнен напрямую
    main()
