"""Экспорт данных карт в Excel."""

import pandas as pd
from pathlib import Path
from typing import List, Optional
from config import DIR_RESULTS, EXCEL_DATE_FORMAT, EXCEL_FILENAME_TEMPLATE, EXCEL_COLUMNS
from models.card import Card


class ExcelExporter:
    """Экспортирует список Card в Excel-файл с формулами."""
    
    def __init__(self, output_dir: Path = DIR_RESULTS):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _make_filename(self, count: int) -> Path:
        """Генерирует имя файла с таймстампом."""
        from datetime import datetime
        timestamp = datetime.now().strftime(EXCEL_DATE_FORMAT)
        filename = EXCEL_FILENAME_TEMPLATE.format(date=timestamp, count=count)
        return self.output_dir / filename
    
    def export(self, cards: List[Card]) -> Optional[Path]:
        """
        Сохраняет карты в Excel.
        
        Args:
            cards: Список объектов Card.
            
        Returns:
            Path к сохранённому файлу или None при ошибке.
        """
        if not cards:
            print("⚠️ Нет данных для экспорта.")
            return None
        
        data = [card.to_excel_dict(i) for i, card in enumerate(cards)]
        df = pd.DataFrame(data, columns=list(EXCEL_COLUMNS.values()))
        
        filepath = self._make_filename(len(cards))
        try:
            df.to_excel(filepath, index=False)
            print(f"💾 Сохранено: \"{filepath}\"")
            return filepath
        except Exception as e:
            print(f"❌ Ошибка экспорта: {e}")
            return None