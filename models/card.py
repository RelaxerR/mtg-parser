"""Модель карты Magic: The Gathering."""

import re
from typing import Dict, Any
from config import MANA_COST_RULES, PT_MULTIPLIER, EXCEL_COLUMNS


class Card:
    """
    Представляет карту MTG с методами расчёта балансовых метрик.
    
    Attributes:
        name: Название карты.
        mana_cost: Строка мана-коста в формате Scryfall.
        text: Текст способностей (Oracle text).
        power_toughness: Строка формата "P/T".
        url: Ссылка на источник.
    """
    
    def __init__(
        self,
        name: str = "",
        mana_cost: str = "",
        text: str = "",
        power_toughness: str = "",
        url: str = ""
    ):
        self.name = name
        self.mana_cost = mana_cost
        self.text = text
        self.power_toughness = power_toughness
        self.url = url
    
    def calculate_mana_points(self) -> int:
        """Рассчитывает стоимость маны по кастомным правилам."""
        total = 0
        symbols = re.findall(r'{(.*?)}', self.mana_cost)
        
        for sym in symbols:
            if sym.isdigit():
                total += self._calc_generic_mana(int(sym))
            elif self._is_colored(sym):
                total += MANA_COST_RULES["colored_cost"]
        return total
    
    def _calc_generic_mana(self, value: int) -> int:
        """Внутренний расчёт для универсальной маны."""
        if value in MANA_COST_RULES["generic"]:
            return MANA_COST_RULES["generic"][value]
        # Линейная формула для значений >= 7
        start = MANA_COST_RULES["generic_linear_start"]
        base = MANA_COST_RULES["generic_linear_base"]
        step = MANA_COST_RULES["generic_linear_step"]
        return base + (value - start) * step
    
    @staticmethod
    def _is_colored(symbol: str) -> bool:
        """Проверяет, является ли символ цветной маной."""
        return symbol.upper() in {'W', 'U', 'B', 'R', 'G'}
    
    def calculate_pt_points(self) -> int:
        """Рассчитывает стоимость показателей силы/выносливости."""
        try:
            if '/' not in self.power_toughness:
                return 0
            p, t = self.power_toughness.strip().split('/')
            power = int(re.search(r'\d+', p).group())
            toughness = int(re.search(r'\d+', t).group())
            return (power + toughness) * PT_MULTIPLIER
        except (ValueError, AttributeError):
            return 0
    
    def to_excel_dict(self, row_num: int) -> Dict[str, Any]:
        """
        Преобразует карту в словарь для Excel-строки.
        
        Args:
            row_num: Номер строки данных (0-based, без учёта заголовка).
        """
        excel_row = row_num + 2  # Excel: 1-based + 1 строка заголовка
        
        return {
            EXCEL_COLUMNS["NAME"]: self.name,
            EXCEL_COLUMNS["MANA_COST"]: self.mana_cost,
            EXCEL_COLUMNS["TEXT"]: self.text,
            EXCEL_COLUMNS["PT"]: self.power_toughness,
            EXCEL_COLUMNS["URL"]: self.url,
            EXCEL_COLUMNS["MANA_POINTS"]: self.calculate_mana_points(),
            EXCEL_COLUMNS["PT_POINTS"]: self.calculate_pt_points(),
            EXCEL_COLUMNS["ABILITY_POINTS"]: 0,  # заглушка
            EXCEL_COLUMNS["TOTAL_POWER"]: f"=G{excel_row}+H{excel_row}",
            EXCEL_COLUMNS["BALANCE"]: f"=I{excel_row}-F{excel_row}",
        }
    
    def __repr__(self) -> str:
        return f"Card('{self.name}', P/T:{self.power_toughness})"