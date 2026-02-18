"""Фасад для запуска полного пайплайна анализа."""

from typing import List
from models.card import Card
from parsers.html_extractor import HTMLCardParser
from services.downloader import CardDownloader
from services.excel_exporter import ExcelExporter


class MTGCardAnalyzer:
    """
    Главный класс-фасад: координирует загрузку, парсинг и экспорт.
    
    Пример использования:
        analyzer = MTGCardAnalyzer()
        cards = analyzer.run(10)
    """
    
    def __init__(self):
        self.downloader = CardDownloader()
        self.parser = HTMLCardParser()
        self.exporter = ExcelExporter()
        self.cards: List[Card] = []
    
    def _print_report(self) -> None:
        """Выводит краткий отчёт в консоль."""
        print("\n📊 Обработано карт:", len(self.cards))
        print("-" * 50)
        for i, card in enumerate(self.cards, 1):
            print(f"{i:2d}. {card.name:25s} | {card.mana_cost:10s} | {card.power_toughness}")
        print("-" * 50)
    
    def run(self, count: int) -> List[Card]:
        """
        Запускает полный цикл анализа.
        
        Args:
            count: Количество карт для обработки.
            
        Returns:
            Список проанализированных объектов Card.
        """
        print(f"🚀 Анализ {count} карт запущен...\n")
        
        # 1. Загрузка
        raw_data = self.downloader.fetch_batch(count)
        if not raw_data:
            print("⚠️ Не загружено ни одной карты.")
            return []
        
        # 2. Парсинг
        self.cards = [self.parser.parse(html, url) for html, url in raw_data]
        
        # 3. Отчёт
        self._print_report()
        
        # 4. Экспорт
        self.exporter.export(self.cards)
        
        return self.cards