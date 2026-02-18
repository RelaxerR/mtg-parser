"""Парсер HTML-страниц Scryfall."""

from bs4 import BeautifulSoup
from typing import Union
from config import SELECTORS
from models.card import Card


class HTMLCardParser:
    """Извлекает данные карты из HTML-контента Scryfall."""
    
    @staticmethod
    def _find_text(soup: BeautifulSoup, selector: str) -> str:
        """Вспомогательный метод: поиск текста по CSS-селектору."""
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else ""
    
    @staticmethod
    def _extract_mana_symbols(soup: BeautifulSoup) -> str:
        """Собирает мана-символы из <abbr> тегов."""
        container = soup.select_one(SELECTORS["MANA_COST"])
        if not container:
            return ""
        symbols = container.find_all('abbr')
        return "".join(sym.get_text(strip=True) for sym in symbols)
    
    @staticmethod
    def _extract_oracle_text(soup: BeautifulSoup) -> str:
        """Извлекает текст правил, объединяя параграфы."""
        container = soup.select_one(SELECTORS["ORACLE_TEXT"])
        if not container:
            return ""
        paragraphs = container.find_all('p')
        return "\n".join(p.get_text(strip=True) for p in paragraphs)
    
    @classmethod
    def parse(cls, html_content: str, source_url: str) -> Card:
        """
        Factory-метод: создаёт Card из raw HTML.
        
        Args:
            html_content: Исходный HTML страницы.
            source_url: URL источника для отслеживания.
            
        Returns:
            Card: Заполненный объект карты.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        return Card(
            name=cls._find_text(soup, SELECTORS["CARD_NAME"]) or "Unknown",
            mana_cost=cls._extract_mana_symbols(soup),
            text=cls._extract_oracle_text(soup),
            power_toughness=cls._find_text(soup, SELECTORS["CARD_STATS"]) or "0/0",
            url=source_url
        )