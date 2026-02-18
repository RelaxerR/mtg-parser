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
    # Универсальная мана {0}, {1}, {2}...
    "generic": {0: 0, 1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 11},
    "generic_linear_start": 6,  # от 7+ применяется линейная формула
    "generic_linear_base": 11,
    "generic_linear_step": 3,
    
    # Цветная мана {W}, {W}{W}, {W}{W}{W}...
    "colored_base": {1: 2, 2: 5, 3: 11},  # 1=2, 2=5, 3=11
    "colored_linear_start": 3,  # от 4+ применяется линейная формула
    "colored_linear_base": 11,
    "colored_linear_step": 6,  # 11 + 6*(N-3) для 4+
}

PT_MULTIPLIER = 2  # коэффициент для P/T: (P+T) * 2

# === Оценка способностей ===

# Ключевые слова и их стоимость
KEYWORD_ABILITIES = {
    # Уклонение (Evasion)
    'flying': 2,
    'menace': 1,
    'unblockable': 4,
    "can't be blocked": 4,
    'cannot be blocked': 4,
    'shadow': 3,
    'fear': 2,
    'intimidate': 2,
    'horsemanship': 3,
    'skulk': 2,
    'landwalk': 2,
    'swampwalk': 2,
    'islandwalk': 2,
    'mountainwalk': 2,
    'forestwalk': 2,
    'plainswalk': 2,
    'snowswampwalk': 2,
    'snowforestwalk': 2,
    'snowmountainwalk': 2,
    'snowislandwalk': 2,
    'snowplainswalk': 2,
    
    # Защита (Protection)
    'hexproof': 3,
    'shroud': 2,
    'indestructible': 3,
    'protection from': 2,
    'ward': 2,
    'phasing': 2,
    'phase out': 2,
    'phase in': 2,
    
    # Боевые способности
    'first strike': 1,
    'double strike': 3,
    'deathtouch': 2,
    'lifelink': 2,
    'trample': 1,
    'vigilance': 1,
    'haste': 1,
    'reach': 1,
    'defender': -1,
    'banding': 1,
    'rampage': 1,
    'flanking': 1,
    'bushido': 1,
    'exalted': 2,
    'prowess': 2,
    'myriad': 4,
    'infect': 3,
    'wither': 2,
    'toxic': 2,
    
    # Дополнительные ключевые слова
    'flash': 1,
    'foretell': 2,
    'disturb': 2,
    'embalm': 2,
    'eternalize': 3,
    'mutate': 2,
    'manifest': 2,
    'morph': 2,
    'megamorph': 3,
    'evoke': 2,
    'kicker': 1,
    'multikicker': 2,
    'overload': 2,
    'replicate': 2,
    'buyback': 2,
    'rebound': 2,
    'miracle': 3,
    'delve': 2,
    'convoke': 2,
    'improvise': 2,
    'assist': 1,
    'entwine': 1,
    'modular': 2,
    'soulshift': 2,
    'spiritcraft': 1,
    'ninjutsu': 3,
    'ninjutsu': 3,
    'sneak': 2,
    'persist': 2,
    'undying': 3,
    'unearth': 2,
    'retrace': 1,
    'split second': 3,
    'suspend': 2,
    'vanishing': 1,
    'storm': 7,
    'cascade': 6,
    'fling': 2,
    'madness': 2,
    'hellbent': 1,
    'threshold': 1,
    'metalcraft': 1,
    'ferocious': 1,
    'heroic': 2,
    'battalion': 2,
    'landfall': 2,
    'raid': 1,
    'morbid': 1,
    'radiance': 2,
    'domain': 1,
    'coalition': 1,
    'pack tactics': 2,
    'offspring': 2,
    'training': 1,
    'mentor': 1,
    'companion': 3,
    'partner': 2,
    'choose a background': 2,
    'doctor companion': 2,
    'the ring tempts you': 2,
    'venture into the dungeon': 3,
    'stun counter': 1,
    'blitz': 2,
    'disturb': 2,
    'ascend': 2,
    'city blessing': 2,
    'exploit': 2,
    'renown': 2,
    'awaken': 2,
    'jump-start': 2,
    'spectacle': 2,
    'aftermath': 2,
    'embalm': 2,
    'eternalize': 3,
}

# Паттерны триггерных способностей
TRIGGER_PATTERNS = {
    # ETB эффекты
    r'when.*enters': 3,
    r'when.*enters.*battlefield': 3,
    r'when.*comes.*battlefield': 3,
    r'as.*enters': 2,
    r'enter.*with.*counter': 2,
    
    # Триггеры атаки/блока
    r'whenever.*attacks': 2,
    r'whenever.*blocks': 1,
    r'whenever.*becomes.*blocked': 2,
    r'whenever.*deals.*damage': 3,
    r'whenever.*deals.*combat.*damage': 3,
    r'whenever.*deals.*combat.*damage.*to.*player': 4,
    r'whenever.*is.*blocked': 1,
    r'whenever.*attacks.*alone': 2,
    
    # Триггеры смерти
    r'when.*dies': 2,
    r'when.*is put into.*graveyard': 2,
    r'when.*leaves.*battlefield': 2,
    r'when.*is exiled': 2,
    r'when.*is sacrificed': 2,
    
    # Триггеры разыгрывания
    r'whenever you cast': 3,
    r'whenever.*spell.*cast': 2,
    r'whenever.*instant.*sorcery.*cast': 3,
    r'whenever.*creature.*spell.*cast': 3,
    r'whenever.*noncreature.*spell.*cast': 2,
    r'whenever.*artifact.*spell.*cast': 2,
    r'whenever.*enchantment.*spell.*cast': 2,
    
    # Триггеры начала/конца хода
    r'at.*beginning.*upkeep': 2,
    r'at.*beginning.*end step': 2,
    r'at.*beginning.*combat': 2,
    r'at.*beginning.*your.*combat': 2,
    r'at.*beginning.*each.*end step': 3,
    r'at.*beginning.*each.*upkeep': 3,
    r'at.*beginning.*each.*combat': 3,
    r'at.*beginning.*of.*your.*turn': 2,
    r'at.*beginning.*of.*each.*player.*turn': 3,
    
    # Триггеры жизней/маны
    r'whenever you gain.*life': 2,
    r'whenever.*life.*gained': 2,
    r'whenever.*opponent.*loses.*life': 2,
    r'whenever.*mana.*produced': 2,
    r'whenever.*land.*enters': 2,
    r'whenever.*basic.*land.*enters': 2,
    
    # Триггеры карт
    r'whenever.*draw.*card': 3,
    r'whenever.*card.*drawn': 2,
    r'whenever.*discard.*card': 2,
    r'whenever.*card.*put.*graveyard': 2,
    r'whenever.*creature.*card.*graveyard': 3,
    
    # Триггеры токенов/счётчиков
    r'whenever.*token.*enters': 2,
    r'whenever.*creature.*enters.*under.*control': 3,
    r'whenever.*counter.*put': 2,
    r'whenever.*\+1/\+1.*counter': 2,
    
    # Триггеры типа/подтипа
    r'whenever.*Elf.*enters': 2,
    r'whenever.*Goblin.*enters': 2,
    r'whenever.*Dragon.*enters': 3,
    r'whenever.*Zombie.*enters': 2,
    r'whenever.*another.*creature': 2,
    r'whenever.*one or more.*creatures': 3,
    r'whenever.*nontoken.*creature': 2,
    
    # Триггеры мутации/превращения
    r'whenever.*mutates': 3,
    r'whenever.*transform': 3,
    r'whenever.*turned face up': 2,
    
    # Триггеры Ring/Doctor
    r'the Ring tempts you': 2,
    r'whenever.*Ring.*tempts': 2,
    r'whenever.*Doctor.*deals': 2,
}

# Паттерны эффектов
EFFECT_PATTERNS = {
    # Карточное преимущество
    r'draw.*card': 4,
    r'draw.*cards': 5,
    r'draw.*X.*cards': 6,
    r'scry.*\d*': 1,
    r'surveil.*\d*': 1,
    r'mill.*\d*': 1,
    r'look.*top.*card': 1,
    r'look.*top.*cards': 2,
    r'reveal.*top.*cards': 2,
    r'put.*top.*card.*hand': 3,
    r'put.*card.*hand.*library': 2,
    
    # Удаление
    r'destroy.*target.*creature': 5,
    r'destroy.*all.*creatures': 8,
    r'destroy.*target.*permanent': 6,
    r'destroy.*all.*permanents': 10,
    r'exile.*target.*creature': 6,
    r'exile.*all.*creatures': 9,
    r'exile.*target.*permanent': 7,
    r'exile.*all.*permanents': 12,
    r'sacrifice.*target.*creature': 3,
    r'sacrifice.*a.*creature': 2,
    r'return.*to.*hand': 3,
    r'return.*to.*owner.*hand': 3,
    r'put.*on.*top.*library': 1,
    r'put.*on.*bottom.*library': 1,
    
    # Создание токенов
    r'create.*token': 3,
    r'create.*a.*\d+/\d+.*token': 4,
    r'create.*two.*\d+/\d+.*token': 7,
    r'create.*three.*\d+/\d+.*token': 10,
    r'create.*X.*\d+/\d+.*token': 5,
    r'create.*Treasure.*token': 3,
    r'create.*Food.*token': 2,
    r'create.*Clue.*token': 2,
    r'create.*Blood.*token': 2,
    r'create.*Map.*token': 2,
    r'create.*Gold.*token': 3,
    r'create.*Servo.*token': 2,
    r'create.*Spirit.*token': 3,
    r'create.*Zombie.*token': 3,
    r'create.*Dragon.*token': 5,
    r'create.*Elemental.*token': 3,
    r'create.*Saproling.*token': 2,
    r'create.*Plant.*token': 2,
    r'create.*Insect.*token': 2,
    r'create.*Bird.*token': 2,
    r'create.*Cat.*token': 2,
    r'create.*Wolf.*token': 3,
    r'create.*Knight.*token': 3,
    r'create.*Soldier.*token': 2,
    r'create.*Human.*token': 2,
    r'create.*Elf.*token': 2,
    r'create.*Goblin.*token': 2,
    r'create.*Thopter.*token': 3,
    r'create.*Construct.*token': 4,
    r'create.*Phyrexian.*token': 3,
    r'create.*Incubator.*token': 3,
    
    # Поиск библиотеки
    r'search.*library': 4,
    r'search.*library.*creature': 5,
    r'search.*library.*land': 3,
    r'search.*library.*basic.*land': 3,
    r'search.*library.*artifact': 4,
    r'search.*library.*enchantment': 4,
    r'search.*library.*instant.*sorcery': 4,
    r'search.*library.*card.*name': 5,
    r'search.*library.*card.*type': 4,
    r'search.*library.*card.*subtype': 4,
    r'search.*library.*card.*mana value': 5,
    r'fetch.*land': 3,
    
    # Рекурсия
    r'return.*from.*graveyard.*to.*hand': 4,
    r'return.*from.*graveyard.*to.*battlefield': 6,
    r'return.*from.*exile.*to.*hand': 5,
    r'return.*from.*exile.*to.*battlefield': 7,
    r'cast.*from.*graveyard': 4,
    r'cast.*from.*exile': 5,
    r'play.*from.*graveyard': 4,
    r'play.*from.*exile': 5,
    
    # Контроль
    r'gain control.*target.*permanent': 7,
    r'gain control.*target.*creature': 6,
    r'gain control.*until.*end.*turn': 5,
    r'counter.*target.*spell': 5,
    r'counter.*target.*creature.*spell': 6,
    r'counter.*target.*noncreature.*spell': 4,
    r'counter.*target.*activated.*ability': 4,
    r'counter.*target.*triggered.*ability': 4,
    r'tap.*target.*creature': 2,
    r'tap.*target.*permanent': 3,
    r'untap.*target.*creature': 2,
    r'untap.*all.*creatures': 4,
    r'prevent.*damage': 2,
    r'regenerate.*target.*creature': 3,
    r'phase out.*target.*permanent': 3,
    
    # Урон
    r'deals.*\d+.*damage.*to.*any.*target': 3,
    r'deals.*\d+.*damage.*to.*target.*creature': 2,
    r'deals.*\d+.*damage.*to.*target.*player': 3,
    r'deals.*damage.*equal.*power': 4,
    r'deals.*damage.*equal.*toughness': 3,
    r'deals.*damage.*equal.*mana value': 4,
    r'deals.*damage.*divided.*among': 3,
    r'deals.*damage.*to.*each.*creature': 5,
    r'deals.*damage.*to.*each.*opponent': 4,
    r'deals.*damage.*to.*each.*player': 5,
    r'deals.*damage.*to.*all.*creatures': 6,
    r'fight.*target.*creature': 4,
    
    # Жизни
    r'you gain.*life': 1,
    r'you gain.*X.*life': 2,
    r'each.*player.*gains.*life': 2,
    r'target.*player.*gains.*life': 1,
    r'you lose.*life': -1,
    r'you lose.*X.*life': -2,
    r'each.*opponent.*loses.*life': 2,
    r'target.*opponent.*loses.*life': 2,
    r'your.*life.*total.*becomes': 3,
    
    # Маны
    r'add.*mana': 2,
    r'add.*{[WUBRGC]}': 1,
    r'add.*{[WUBRGC]}{[WUBRGC]}': 2,
    r'add.*three.*mana.*any.*color': 4,
    r'add.*mana.*any.*color': 3,
    r'add.*mana.*any.*type': 4,
    r'add.*colorless.*mana': 1,
    r'add.*energy.*counter': 2,
    r'add.*rad.*counter': 2,
    
    # Счётчики
    r'\+1/\+1.*counter': 2,
    r'-1/-1.*counter': 2,
    r'put.*\+1/\+1.*counter': 2,
    r'put.*X.*\+1/\+1.*counter': 3,
    r'put.*counter.*on.*target.*creature': 2,
    r'put.*counter.*on.*each.*creature': 4,
    r'remove.*counter': 1,
    r'move.*counter': 2,
    r'proliferate': 3,
    r'proliferate.*X.*times': 4,
    r'incubate.*\d*': 3,
    r'adapt.*\d*': 2,
    
    # Мощные эффекты
    r'extra turn': 10,
    r'additional.*turn': 10,
    r'extra.*combat.*phase': 8,
    r'additional.*combat.*phase': 8,
    r'additional.*main.*phase': 6,
    r'additional.*phase': 7,
    r'you win the game': 15,
    r'opponent.*loses the game': 12,
    r'copy.*target.*spell': 5,
    r'copy.*target.*instant.*sorcery': 6,
    r'copy.*spell.*you.*control': 5,
    r'cascade': 6,
    r'storm': 7,
    r'you may cast.*without paying.*mana cost': 5,
    r'you may play.*without paying.*mana cost': 5,
    r'foretell.*\d*': 2,
    r'demonstrate': 3,
    r'choose.*Background': 2,
    r'partner.*with': 2,
    
    # Усиления существ
    r'gets.*\+X/\+X.*until end.*turn': 3,
    r'gets.*\+1/\+1.*until end.*turn': 1,
    r'gets.*\+2/\+2.*until end.*turn': 2,
    r'gains.*flying.*until end.*turn': 1,
    r'gains.*haste.*until end.*turn': 1,
    r'gains.*indestructible.*until end.*turn': 3,
    r'gains.*protection.*until end.*turn': 2,
    r'gains.*all.*abilities': 4,
    r'becomes.*copy.*of.*target.*creature': 6,
    r'becomes.*X/X.*creature': 3,
    
    # Контроль хода/фаз
    r'skip.*untap.*step': 3,
    r'skip.*draw.*step': 2,
    r'skip.*combat.*phase': 4,
    r'end.*of.*turn.*effect': 1,
    r'at.*next.*end step': 1,
    r'at.*beginning.*of.*next.*end step': 2,
    
    # Специальные механики
    r'earthbend.*\d*': 2,
    r'waterbend.*\d*': 2,
    r'firebend.*\d*': 2,
    r'airbend.*\d*': 2,
    r'crank.*this.*Contraption': 2,
    r'assemble.*a.*Contraption': 3,
    r'open.*an.*Attraction': 3,
    r'claim.*the.*prize': 4,
    r'visit.*—': 2,
    r'roll.*a.*d20': 2,
    r'roll.*a.*d6': 1,
    r'roll.*a.*d4': 1,
}

# Стоимость активируемых способностей
ACTIVATED_ABILITY_COST = {
    'tap_only': 2,          # {T}: effect
    'tap_mana_1': 3,        # {1}{T}: effect
    'tap_mana_2_3': 4,      # {2-3}{T}: effect
    'tap_mana_4_plus': 2,   # {4+}{T}: effect
    'sacrifice': 3,         # Sacrifice: effect
    'discard': 2,           # Discard: effect
    'pay_life': 1,          # Pay X life: effect
    'exile_card': 2,        # Exile card from graveyard: effect
    'remove_counter': 2,    # Remove counter: effect
    'untap_self': 1,        # {T}, untap this: effect
    'crew': 2,              # Crew N: effect (for Vehicles)
    'saddle': 2,            # Saddle N: effect (for Mounts)
    'station': 2,           # Station: effect (for Spacecraft)
    'earthbend_cost': 2,    # Earthbend cost
    'waterbend_cost': 2,    # Waterbend cost
}

# Паттерны для недостатков карт
DRAWBACK_PATTERNS = {
    r"can't attack": -2,
    r"cannot attack": -2,
    r"can't block": -1,
    r"cannot block": -1,
    r"doesn't untap": -3,
    r"does not untap": -3,
    r"won't untap": -3,
    r"will not untap": -3,
    r"sacrifice.*at.*beginning.*upkeep": -2,
    r"sacrifice.*at.*beginning.*end step": -2,
    r"sacrifice.*at.*end.*turn": -2,
    r"sacrifice.*this.*turn": -2,
    r"you lose.*life": -1,
    r"you lose.*X.*life": -2,
    r"opponent.*gains.*life": -1,
    r"enters.*tapped": -1,
    r"comes.*tapped": -1,
    r"cumulative upkeep": -2,
    r"echo.*\d*": -1,
    r"can't be regenerated": -1,
    r"cannot be regenerated": -1,
    r"attacks.*each.*combat.*if.*able": -1,
    r"must.*attack.*if.*able": -1,
    r"can't attack.*alone": -1,
    r"cannot attack.*alone": -1,
    r"only.*attack.*player.*it.*has.*attacked": -2,
    r"exile.*at.*beginning.*end step": -2,
    r"return.*to.*owner.*hand.*end step": -2,
    r"shuffle.*into.*owner.*library": -2,
    r"you.*skip.*your.*next.*turn": -5,
    r"you.*skip.*your.*next.*two.*turns": -10,
    r"opponent.*draws.*card": -2,
    r"target.*opponent.*creates.*token": -2,
    r"this.*spell.*costs.*more.*to.*cast": -1,
    r"as.*additional.*cost.*sacrifice": -2,
    r"as.*additional.*cost.*discard": -1,
    r"as.*additional.*cost.*pay.*life": -1,
    r"madness.*cost.*only.*when.*discarded": 0,
    r"flashback.*exile.*after.*cast": 0,
    r"can.*only.*be.*cast.*during.*combat": -1,
    r"can.*only.*cast.*creature.*spells": -2,
    r"can.*only.*cast.*instant.*sorcery": -2,
    r"noncreature.*spells.*cost.*more": -1,
    r"spells.*you.*cast.*cost.*more": -2,
    r"opponents.*can't.*lose.*game": -5,
    r"you.*can't.*win.*game": -5,
    r"lose.*the.*game.*if.*condition": -8,
}

# Бонусы за синергию
SYNERGY_BONUSES = {
    'draw_discard': {'keywords': ['draw', 'discard'], 'bonus': 2},
    'sacrifice_token': {'keywords': ['sacrifice', 'create', 'token'], 'bonus': 2},
    'exile_return': {'keywords': ['exile', 'return'], 'bonus': 2},
    'landfall_mana': {'keywords': ['landfall', 'add', 'mana'], 'bonus': 2},
    'life_gain_benefit': {'keywords': ['gain', 'life', 'lifelink'], 'bonus': 2},
    'counter_synergy': {'keywords': ['counter', '+1/+1', 'proliferate'], 'bonus': 3},
    'artifact_mana': {'keywords': ['artifact', 'add', 'mana', 'improvise', 'convoke'], 'bonus': 2},
    'graveyard_matters': {'keywords': ['graveyard', 'mill', 'return', 'from.*graveyard'], 'bonus': 2},
    'token_army': {'keywords': ['create', 'token', 'army', 'each.*creature'], 'bonus': 3},
    'commander_synergy': {'keywords': ['commander', 'color.*identity', 'legendary'], 'bonus': 2},
    'multicolor_synergy': {'keywords': ['multicolored', 'hybrid', 'any.*color'], 'bonus': 2},
    'storm_cascade': {'keywords': ['storm', 'cascade', 'replicate', 'copy.*spell'], 'bonus': 4},
}

# Настройки расчёта способностей
ABILITY_CALCULATION = {
    'max_duplicate_triggers': 3,  # Maximum identical triggers to count
    'max_activated_abilities': 2,  # Maximum identical activated abilities to count
    'multiple_triggers_bonus': 3,  # Bonus for 3+ different triggers
    'multiple_triggers_threshold': 3,  # Threshold for bonus
    'token_value_multiplier': 1.2,  # Multiplier for token creation value
    'removal_efficiency_bonus': 1.5,  # Bonus for efficient removal
    'card_advantage_weight': 1.3,  # Weight for card draw/search effects
}

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