"""Фасад для запуска полного пайплайна анализа."""

from typing import List, Optional, Tuple
from tqdm import tqdm
from models.card import Card
from parsers.html_extractor import HTMLCardParser
from services.downloader import CardDownloader
from services.excel_exporter import ExcelExporter


class MTGCardAnalyzer:
    """
    Главный класс-фасад: координирует загрузку, парсинг и экспорт.
    
    Поддерживает два режима:
    - Онлайн: загрузка с Scryfall
    - Офлайн: загрузка из локального кэша
    """
    
    def __init__(self):
        self.downloader = CardDownloader()
        self.parser = HTMLCardParser()
        self.exporter = ExcelExporter()
        self.cards: List[Card] = []
    
    def _print_report(self) -> None:
        """Выводит краткий отчёт в консоль."""
        print("\n📊 Обработано карт:", len(self.cards))
        print("-" * 70)
        
        for i, card in enumerate(self.cards, 1):
            name = card.name[:25].ljust(25)
            mana = card.mana_cost[:12].ljust(12)
            pt = card.power_toughness[:5].ljust(5)
            print(f"{i:2d}. {name} | {mana} | {pt}")
        
        print("-" * 70)
    
    def run_online(self, count: int) -> List[Card]:
        """
        Запускает анализ с загрузкой из интернета.
        
        Args:
            count: Количество карт для загрузки.
            
        Returns:
            Список проанализированных объектов Card.
        """
        print(f"🚀 Онлайн-анализ {count} карт запущен...\n")
        
        raw_data = self.downloader.fetch_batch(count)
        if not raw_data:
            print("⚠️ Не загружено ни одной карты.")
            return []
        
        self._process_data(raw_data)
        return self.cards
    
    def run_offline(self, limit: Optional[int] = None) -> List[Card]:
        """
        Запускает анализ с загрузкой из локального кэша.
        
        Args:
            limit: Максимальное количество карт (None = все).
            
        Returns:
            Список проанализированных объектов Card.
        """
        cache_count = self.downloader.get_cache_count()
        
        if cache_count == 0:
            print("⚠️ Кэш пуст — сначала запустите онлайн-режим.")
            return []
        
        print(f"🚀 Офлайн-анализ кэша ({cache_count} файлов)...\n")
        
        raw_data = self.downloader.load_from_cache(limit)
        if not raw_data:
            print("⚠️ Не удалось загрузить данные из кэша.")
            return []
        
        self._process_data(raw_data)
        return self.cards
    
    def _process_data(self, raw_data: List[Tuple[str, str]]) -> None:
        """
        Обрабатывает сырые данные: парсинг и экспорт.
        
        Args:
            raw_data: Список кортежей (html_content, url).
        """
        # Парсинг
        print("\n🔍 Парсинг данных...")
        self.cards = []
        for html, url in tqdm(raw_data, desc="🔍 Парсинг", unit="карта", colour="cyan", ncols=80):
            card = self.parser.parse(html, url)
            self.cards.append(card)
        
        # Отчёт
        self._print_report()
        
        # Экспорт
        print("\n💾 Экспорт в Excel...")
        self.exporter.export(self.cards)
    
    def clear_cache(self) -> int:
        """Очищает кэш HTML-файлов."""
        count = self.downloader.clear_cache()
        print(f"🗑️ Удалено {count} файлов из кэша.")
        return count