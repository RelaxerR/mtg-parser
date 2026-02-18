"""Модель карты Magic: The Gathering."""

import re
from typing import Dict, Any
from config import MANA_COST_RULES, PT_MULTIPLIER, EXCEL_COLUMNS


class Card:
    """
    Представляет карту MTG с методами расчёта балансовых метрик.
    """
    
    MANA_COLORS = {'W', 'U', 'B', 'R', 'G'}
    
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
        """
        Рассчитывает стоимость маны по кастомным правилам.
        
        Returns:
            int: Общая стоимость маны в очках.
        """
        total = 0
        symbols = re.findall(r'{(.*?)}', self.mana_cost)
        
        # Считаем количество цветной маны по каждому цвету
        color_counts = {color: 0 for color in self.MANA_COLORS}
        
        for sym in symbols:
            if sym.isdigit():
                # Универсальная мана: {0}, {1}, {2}...
                total += self._calc_generic_mana(int(sym))
            elif '/' in sym:
                # Гибридная мана {W/U} или спец. символы — игнорируется
                continue
            elif sym.upper() in self.MANA_COLORS:
                # Цветная мана: {W}, {G}, {B}...
                color_counts[sym.upper()] += 1
        
        # Рассчитываем стоимость цветной маны для каждого цвета
        for color, count in color_counts.items():
            if count > 0:
                total += self._calc_colored_mana(count)
        
        return total
    
    def _calc_generic_mana(self, value: int) -> int:
        """Рассчитывает стоимость универсальной маны."""
        if value in MANA_COST_RULES["generic"]:
            return MANA_COST_RULES["generic"][value]
        
        start = MANA_COST_RULES["generic_linear_start"]
        base = MANA_COST_RULES["generic_linear_base"]
        step = MANA_COST_RULES["generic_linear_step"]
        return base + (value - start) * step
    
    def _calc_colored_mana(self, count: int) -> int:
        """
        Рассчитывает стоимость цветной маны одного цвета.
        
        Формула:
        - 1 = 2 очка
        - 2 = 5 очков
        - 3 = 11 очков
        - 4+ = 11 + 6×(N-3)
        
        Args:
            count: Количество мана-символов одного цвета.
            
        Returns:
            int: Стоимость в очках.
        """
        if count in MANA_COST_RULES["colored_base"]:
            return MANA_COST_RULES["colored_base"][count]
        
        start = MANA_COST_RULES["colored_linear_start"]
        base = MANA_COST_RULES["colored_linear_base"]
        step = MANA_COST_RULES["colored_linear_step"]
        return base + (count - start) * step
    
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
        """Преобразует карту в словарь для Excel-строки."""
        excel_row = row_num + 2
        
        return {
            EXCEL_COLUMNS["NAME"]: self.name,
            EXCEL_COLUMNS["MANA_COST"]: self.mana_cost,
            EXCEL_COLUMNS["TEXT"]: self.text,
            EXCEL_COLUMNS["PT"]: self.power_toughness,
            EXCEL_COLUMNS["URL"]: self.url,
            EXCEL_COLUMNS["MANA_POINTS"]: self.calculate_mana_points(),
            EXCEL_COLUMNS["PT_POINTS"]: self.calculate_pt_points(),
            EXCEL_COLUMNS["ABILITY_POINTS"]: 0,
            EXCEL_COLUMNS["TOTAL_POWER"]: f"=G{excel_row}+H{excel_row}",
            EXCEL_COLUMNS["BALANCE"]: f"=I{excel_row}-F{excel_row}",
        }
    
    def __repr__(self) -> str:
        return f"Card('{self.name}', P/T:{self.power_toughness})"