"""Сервис загрузки карт с Scryfall с кэшированием."""

import time
import requests
from pathlib import Path
from typing import Optional, List, Tuple
from tqdm import tqdm
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
        """
        Загружает пакет карт с прогресс-баром.
        
        Args:
            count: Количество карт для загрузки.
            
        Returns:
            List[Tuple]: Список кортежей (html_content, url).
        """
        results = []
        
        with tqdm(
            total=count,
            desc="📥 Загрузка карт",
            unit="карта",
            colour="green",
            ncols=80
        ) as pbar:
            for i in range(count):
                card = self.fetch_one()
                
                if card:
                    results.append(card)
                    pbar.set_postfix({"✅": len(results), "❌": i + 1 - len(results)})
                    pbar.update(1)
                else:
                    pbar.set_postfix({"✅": len(results), "❌": i + 1 - len(results)})
                    pbar.update(1)
                
                time.sleep(self.delay)
        
        return results
    
    def load_from_cache(self, limit: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        Загружает карты из локального кэша HTML.
        
        Args:
            limit: Максимальное количество карт для загрузки (None = все).
            
        Returns:
            List[Tuple]: Список кортежей (html_content, url).
        """
        html_files = sorted(self.cache_dir.glob("card_*.html"))
        
        if not html_files:
            print("⚠️ Кэш пуст — нет сохранённых страниц.")
            return []
        
        if limit:
            html_files = html_files[:limit]
        
        results = []
        print(f"📂 Найдено {len(html_files)} файлов в кэше")
        
        with tqdm(
            total=len(html_files),
            desc="📂 Загрузка из кэша",
            unit="файл",
            colour="cyan",
            ncols=80
        ) as pbar:
            for filepath in html_files:
                try:
                    html_content = filepath.read_text(encoding='utf-8')
                    # Извлекаем URL из имени файла
                    slug = filepath.stem.replace("card_", "")
                    url = f"https://scryfall.com/card/{slug}"
                    results.append((html_content, url))
                    pbar.update(1)
                except Exception as e:
                    print(f"⚠️ Ошибка чтения {filepath.name}: {e}")
                    pbar.update(1)
        
        return results
    
    def get_cache_count(self) -> int:
        """Возвращает количество файлов в кэше."""
        return len(list(self.cache_dir.glob("card_*.html")))
    
    def clear_cache(self) -> int:
        """
        Очищает кэш HTML-файлов.
        
        Returns:
            int: Количество удалённых файлов.
        """
        html_files = list(self.cache_dir.glob("card_*.html"))
        for filepath in html_files:
            filepath.unlink()
        return len(html_files)