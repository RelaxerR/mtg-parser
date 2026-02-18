"""Глобальные настройки и константы приложения."""

from pathlib import Path

# === Пути ===
BASE_DIR = Path(__file__).parent
DIR_RESULTS = BASE_DIR / "results"
DIR_HTML_CACHE = BASE_DIR / "cards_html"

# === Scryfall API ===
SCRYFALL_RANDOM_URL = "https://scryfall.com/random?l=ru"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.1  # секунды между запросами

# === CSS-селекторы для парсинга ===
SELECTORS = {
    "CARD_NAME": "span.card-text-card-name",
    "MANA_COST": "span.card-text-mana-cost",
    "ORACLE_TEXT": "div.card-text-oracle",
    "CARD_STATS": "div.card-text-stats",
}

# === Формулы расчёта баллов ===
MANA_COST_RULES = {
    "generic": {0: 0, 1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 11},
    "generic_linear_start": 6,  # от 7+ применяется линейная формула
    "generic_linear_base": 11,
    "generic_linear_step": 3,
    "colored_cost": 2,  # цена за {W}/{U}/{B}/{R}/{G}
}

PT_MULTIPLIER = 2  # коэффициент для P/T: (P+T) * 2

# === Excel ===
EXCEL_DATE_FORMAT = "%d-%m-%y-%H-%M-%S"
EXCEL_FILENAME_TEMPLATE = "MTG {date} {count} cards.xlsx"

EXCEL_COLUMNS = {
    "NAME": "Название",
    "MANA_COST": "Мана-кост",
    "TEXT": "Описание",
    "PT": "P/T",
    "URL": "URL",
    "MANA_POINTS": "Стоимость маны (m+U)",
    "PT_POINTS": "Стоимость силы (2P+2T)",
    "ABILITY_POINTS": "Стоимость способностей (s)",
    "TOTAL_POWER": "Итоговая мощь",
    "BALANCE": "Баланс",
}