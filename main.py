#!/usr/bin/env python3
"""Точка входа в приложение MTG Card Analyzer."""

import sys
from core.analyzer import MTGCardAnalyzer


def show_menu() -> str:
    """Показывает меню выбора режима."""
    print("\n" + "=" * 50)
    print("🎴 MTG Card Analyzer")
    print("=" * 50)
    print("1. 🌐 Онлайн — загрузка с Scryfall")
    print("2. 📂 Офлайн — загрузка из кэша")
    print("3. 🗑️ Очистить кэш")
    print("4. 📊 Показать статус кэша")
    print("0. ❌ Выход")
    print("=" * 50)
    return input("Выберите режим: ").strip()


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
        return -1


def main():
    """Основная функция приложения."""
    analyzer = MTGCardAnalyzer()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Онлайн режим
            count = get_card_count()
            if count > 0:
                analyzer.run_online(count)
        
        elif choice == "2":
            # Офлайн режим
            limit_input = input("🔢 Сколько карт из кэша (Enter = все)? ").strip()
            limit = int(limit_input) if limit_input.isdigit() else None
            analyzer.run_offline(limit)
        
        elif choice == "3":
            # Очистка кэша
            confirm = input("⚠️ Вы уверены? (y/n): ").strip().lower()
            if confirm == "y":
                analyzer.clear_cache()
        
        elif choice == "4":
            # Статус кэша
            count = analyzer.downloader.get_cache_count()
            print(f"📊 В кэше: {count} карт")
        
        elif choice == "0":
            print("\n👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор, попробуйте снова.")
        
        # Предложение продолжить
        cont = input("\nПродолжить? (y/n): ").strip().lower()
        if cont != "y":
            print("\n👋 До свидания!")
            break
    
    print("\n✨ Готово! Проверьте папку 'results' для отчёта.")


if __name__ == "__main__":
    main()