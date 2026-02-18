"""Сервис загрузки карт с Scryfall с кэшированием."""

import time
import requests
from pathlib import Path
from typing import Optional, List, Tuple
from config import SCRYFALL_RANDOM_URL, REQUEST_DELAY, REQUEST_TIMEOUT, DIR_HTML_CACHE


class CardDownloader:
    """
    Загружает случайные карты с Scryfall и кэширует HTML.
    
    Attributes:
        cache_dir: Директория для сохранения HTML-файлов.
        delay: Пауза между запросами (защита от rate-limit).
    """
    
    def __init__(self, cache_dir: Path = DIR_HTML_CACHE, delay: float = REQUEST_DELAY):
        self.cache_dir = cache_dir
        self.delay = delay
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _save_to_cache(self, html: str, url: str) -> None:
        """Сохраняет HTML-контент в локальный файл."""
        slug = url.rstrip('/').split('/')[-1]
        filepath = self.cache_dir / f"card_{slug}.html"
        filepath.write_text(html, encoding='utf-8')
    
    def fetch_one(self) -> Optional[Tuple[str, str]]:
        """
        Загружает одну случайную карту.
        
        Returns:
            Tuple(html_content, final_url) или None при ошибке.
        """
        try:
            response = requests.get(
                SCRYFALL_RANDOM_URL,
                allow_redirects=True,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            self._save_to_cache(response.text, response.url)
            return response.text, response.url
            
        except requests.RequestException as e:
            print(f"⚠️ Ошибка загрузки: {e}")
            return None
    
    def fetch_batch(self, count: int) -> List[Tuple[str, str]]:
        """Загружает пакет карт с задержкой между запросами."""
        results = []
        for i in range(count):
            print(f"📥 [{i+1}/{count}] ", end="", flush=True)
            card = self.fetch_one()
            if card:
                results.append(card)
                print("✅")
            else:
                print("❌")
            time.sleep(self.delay)
        return results