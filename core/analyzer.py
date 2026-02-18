"""Фасад для запуска полного пайплайна анализа."""

from typing import List
from tqdm import tqdm
from models.card import Card
from parsers.html_extractor import HTMLCardParser
from services.downloader import CardDownloader
from services.excel_exporter import ExcelExporter


class MTGCardAnalyzer:
    """
    Главный класс-фасад: координирует загрузку, парсинг и экспорт.
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
            # Обрезаем длинные названия для красивого вывода
            name = card.name[:25].ljust(25)
            mana = card.mana_cost[:12].ljust(12)
            pt = card.power_toughness[:5].ljust(5)
            print(f"{i:2d}. {name} | {mana} | {pt}")
        
        print("-" * 70)
    
    def run(self, count: int) -> List[Card]:
        """
        Запускает полный цикл анализа.
        
        Args:
            count: Количество карт для обработки.
            
        Returns:
            Список проанализированных объектов Card.
        """
        print(f"🚀 Анализ {count} карт запущен...\n")
        
        # 1. Загрузка (с прогресс-баром в downloader.fetch_batch)
        raw_data = self.downloader.fetch_batch(count)
        if not raw_data:
            print("⚠️ Не загружено ни одной карты.")
            return []
        
        # 2. Парсинг (с прогресс-баром)
        print("\n🔍 Парсинг данных...")
        self.cards = []
        for html, url in tqdm(raw_data, desc="🔍 Парсинг", unit="карта", colour="cyan", ncols=80):
            card = self.parser.parse(html, url)
            self.cards.append(card)
        
        # 3. Отчёт
        self._print_report()
        
        # 4. Экспорт (с прогресс-баром)
        print("\n💾 Экспорт в Excel...")
        self.exporter.export(self.cards)
        
        return self.cards