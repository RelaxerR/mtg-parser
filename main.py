#!/usr/bin/env python3
"""Точка входа в приложение MTG Card Analyzer."""

import sys
from core.analyzer import MTGCardAnalyzer


def get_card_count() -> int:
    """Запрашивает у пользователя количество карт с валидацией."""
    try:
        value = input("🔢 Сколько карт проанализировать? ").strip()
        count = int(value)
        if count <= 0:
            raise ValueError
        return count
    except ValueError:
        print("❌ Ошибка: введите положительное целое число.")
        sys.exit(1)


def main():
    """Основная функция приложения."""
    count = get_card_count()
    
    analyzer = MTGCardAnalyzer()
    analyzer.run(count)
    
    print("\n✨ Готово! Проверьте папку 'results' для отчёта.")


if __name__ == "__main__":
    main()