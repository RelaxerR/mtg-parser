"""Модель карты Magic: The Gathering."""

import re
from typing import Dict, Any, Set, List
from config import (
    MANA_COST_RULES, 
    PT_MULTIPLIER, 
    EXCEL_COLUMNS,
    KEYWORD_ABILITIES,
    TRIGGER_PATTERNS,
    EFFECT_PATTERNS,
    ACTIVATED_ABILITY_COST,
    DRAWBACK_PATTERNS,
    SYNERGY_BONUSES,
    ABILITY_CALCULATION
)


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
    
    def calculate_ability_points(self) -> int:
        """
        Рассчитывает стоимость способностей на основе текста карты.
        
        Учитывает:
        - Ключевые слова (flying, deathtouch, etc.)
        - Триггерные способности (when/whenever/at)
        - Активируемые способности ({T}, {X})
        - Мощные эффекты (extra turn, draw cards, etc.)
        
        Returns:
            int: Суммарная стоимость всех способностей.
        """
        if not self.text or self.text.strip() == "":
            return 0
        
        text_lower = self.text.lower()
        total_points = 0
        
        # 1. Подсчёт ключевых слов
        total_points += self._count_keyword_abilities(text_lower)
        
        # 2. Подсчёт триггерных способностей
        total_points += self._count_trigger_abilities(text_lower)
        
        # 3. Подсчёт эффектов
        total_points += self._count_effect_patterns(text_lower)
        
        # 4. Подсчёт активируемых способностей
        total_points += self._count_activated_abilities(text_lower)
        
        # 5. Бонусы за комбо-эффекты
        total_points += self._calculate_synergy_bonus(text_lower)
        
        # 6. Штрафы за негативные эффекты
        total_points += self._calculate_drawback_penalty(text_lower)
        
        return max(0, total_points)  # Минимум 0
    
    def _count_keyword_abilities(self, text: str) -> int:
        """Подсчитывает очки за ключевые способности."""
        points = 0
        counted_keywords: Set[str] = set()
        
        for keyword, value in KEYWORD_ABILITIES.items():
            if keyword in text and keyword not in counted_keywords:
                points += value
                counted_keywords.add(keyword)
        
        return points
    
    def _count_trigger_abilities(self, text: str) -> int:
        """Подсчитывает очки за триггерные способности."""
        points = 0
        max_duplicates = ABILITY_CALCULATION['max_duplicate_triggers']
        
        for pattern, value in TRIGGER_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Каждый уникальный триггер даёт очки
                points += value * min(len(matches), max_duplicates)
        
        return points
    
    def _count_effect_patterns(self, text: str) -> int:
        """Подсчитывает очки за различные эффекты."""
        points = 0
        counted_effects: Set[str] = set()
        
        for pattern, value in EFFECT_PATTERNS.items():
            if pattern not in counted_effects and re.search(pattern, text, re.IGNORECASE):
                points += value
                counted_effects.add(pattern)
        
        return points
    
    def _count_activated_abilities(self, text: str) -> int:
        """Подсчитывает очки за активируемые способности."""
        points = 0
        max_abilities = ABILITY_CALCULATION['max_activated_abilities']
        
        # Ищем паттерны активации: {T}, {X}, {1}{T}, etc.
        activation_patterns = [
            (r'{t}:', 'tap_only'),
            (r'{[0-9]}{t}:', 'mana_cheap'),
            (r'{[0-9]{2,}}{t}:', 'mana_expensive'),
            (r'sacrifice', 'sacrifice'),
            (r'пожертвуйте', 'sacrifice'),
            (r'discard', 'discard'),
            (r'сбросьте', 'discard'),
        ]
        
        for pattern, cost_type in activation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                points += ACTIVATED_ABILITY_COST[cost_type] * min(len(matches), max_abilities)
        
        return points
    
    def _calculate_synergy_bonus(self, text: str) -> int:
        """Даёт бонусные очки за синергию способностей."""
        bonus = 0
        
        # Проверяем каждую синергию из конфига
        for synergy_name, synergy_data in SYNERGY_BONUSES.items():
            keywords = synergy_data['keywords']
            # Проверяем, есть ли все ключевые слова в тексте
            if all(any(kw in text for kw in keywords[i::len(keywords)//2]) for i in range(len(keywords)//2)):
                bonus += synergy_data['bonus']
        
        # Бонус за множественные триггеры
        threshold = ABILITY_CALCULATION['multiple_triggers_threshold']
        bonus_value = ABILITY_CALCULATION['multiple_triggers_bonus']
        trigger_count = len(re.findall(r'whenever|when|at the beginning|каждый раз|когда|в начале', text, re.IGNORECASE))
        if trigger_count >= threshold:
            bonus += bonus_value
        
        return bonus
    
    def _calculate_drawback_penalty(self, text: str) -> int:
        """Вычитает очки за негативные эффекты."""
        penalty = 0
        
        for pattern, value in DRAWBACK_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                penalty += value
        
        return penalty
    
    # ... остальные методы без изменений ...
    
    def calculate_mana_points(self) -> int:
        """Рассчитывает стоимость маны по кастомным правилам."""
        total = 0
        symbols = re.findall(r'{(.*?)}', self.mana_cost)
        
        generic_total = 0
        colored_total = 0
        
        for sym in symbols:
            if sym.isdigit():
                generic_total += int(sym)
            elif '/' in sym:
                colored_total += 1
            elif sym.upper() in self.MANA_COLORS:
                colored_total += 1
        
        if generic_total > 0:
            total += self._calc_generic_mana(generic_total + colored_total)
        if colored_total > 0:
            total += self._calc_colored_mana(colored_total)
        
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
        """Рассчитывает стоимость цветной маны."""
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
            EXCEL_COLUMNS["ABILITY_POINTS"]: self.calculate_ability_points(),
            EXCEL_COLUMNS["TOTAL_POWER"]: f"=G{excel_row}+H{excel_row}",
            EXCEL_COLUMNS["BALANCE"]: f"=I{excel_row}-F{excel_row}",
        }
    
    def __repr__(self) -> str:
        return f"Card('{self.name}', P/T:{self.power_toughness})"