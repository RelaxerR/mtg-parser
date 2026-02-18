import requests
import time
import os

import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup

class Card:
    def __init__(self, name="", mana_cost="", text="", power_toughness=""):
        self.name = name
        self.mana_cost = mana_cost
        self.text = text
        self.power_toughness = power_toughness

    def to_dict(self):
        """Превращает объект в словарь для Pandas"""
        return {
            "Название": self.name,
            "Мана-кост": self.mana_cost,
            "Описание": self.text,
            "P/T": self.power_toughness
        }

    def __repr__(self):
        return f"Card(Name: {self.name}, Cost: {self.mana_cost}, P/T: {self.power_toughness})"

class ScryfallParser:
    def __init__(self):
        self.cards_list = []

    def save_to_excel(self):
        """Создает DataFrame и сохраняет его в Excel с динамическим именем"""
        if not self.cards_list:
            print("Список карт пуст, нечего сохранять.")
            return

        # 1. Создаем папку results, если её нет
        if not os.path.exists('results'):
            os.makedirs('results')

        # 2. Формируем имя файла: MTG dd-mm-yy N cards.xlsx
        current_date = datetime.now().strftime("%d-%m-%y")
        n_cards = len(self.cards_list)
        filename = f"results/MTG {current_date} {n_cards} cards.xlsx"

        # 3. Создаем данные для таблицы
        data = [card.to_dict() for card in self.cards_list]
        df = pd.DataFrame(data)
        
        # 4. Сохраняем
        try:
            df.to_excel(filename, index=False)
            print(f"Данные успешно сохранены в: {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении Excel: {e}")

    def parse_card_page(self, html_content):
        """Основной метод анализа страницы"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Создаем объект карты и заполняем его через подметоды
        new_card = Card(
            name=self._extract_name(soup),
            mana_cost=self._extract_mana_cost(soup),
            text=self._extract_description(soup),
            power_toughness=self._extract_pt(soup)
        )
        
        self.cards_list.append(new_card)
        return new_card

    def _extract_name(self, soup):
        # Ищем тег span с нужным классом
        name_tag = soup.find('span', class_='card-text-card-name')
        
        if name_tag:
            # .get_text() забирает текст, .strip() убирает лишние переносы и пробелы
            return name_tag.get_text().strip()
        
        return "Unknown Name"

    def _extract_mana_cost(self, soup):
        # Ищем контейнер со всеми символами маны
        mana_container = soup.find('span', class_='card-text-mana-cost')
        
        if mana_container:
            # На Scryfall каждый символ маны лежит в своем теге <abbr>
            # Собираем их все в одну строку, например "{3}{W}"
            symbols = mana_container.find_all('abbr')
            cost_string = "".join([sym.get_text().strip() for sym in symbols])
            return cost_string
        
        return "" # Если мана-коста нет (например, у земель)


    def _extract_description(self, soup):
        # Ищем основной контейнер с текстом правил
        oracle_div = soup.find('div', class_='card-text-oracle')
        
        if oracle_div:
            # Находим все параграфы <p> внутри этого блока
            paragraphs = oracle_div.find_all('p')
            
            # Собираем текст из всех параграфов, разделяя их переносом строки
            full_text = "\n".join([p.get_text().strip() for p in paragraphs])
            return full_text
        
        return "" # Если способностей нет (например, обычное существо без текста)

    def _extract_pt(self, soup):
        # Ищем блок со статами
        stats_div = soup.find('div', class_='card-text-stats')
        
        if stats_div:
            # Очищаем от пробелов и переносов
            return stats_div.get_text().strip()
        
        return "0/0" # Для заклинаний или артефактов без статов

def download_and_parse_cards(n):
    # Создаем папку для сохранения страниц, если её нет
    if not os.path.exists('cards_html'):
        os.makedirs('cards_html')

    base_url = "https://scryfall.com/random"
    parser = ScryfallParser() # Создаем экземпляр нашего парсера
    
    for i in range(n):
        try:
            response = requests.get(base_url, allow_redirects=True)
            
            if response.status_code == 200:
                html_content = response.text
                
                # 1. Сохраняем файл (как и раньше)
                card_url_slug = response.url.split('/')[-1].split('?')[0]
                file_name = f"cards_html/card_{card_url_slug}.html"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # 2. ПАРСИМ страницу и добавляем объект Card в список внутри parser.cards_list
                parser.parse_card_page(html_content)
                
                print(f"[{i+1}/{n}] Обработана карта: {card_url_slug}")
            else:
                print(f"Ошибка при загрузке: {response.status_code}")
                
        except Exception as e:
            print(f"Произошла ошибка при обработке: {e}")
        
        time.sleep(0.1)
    
    # Возвращаем итоговый список объектов Card
    parser.save_to_excel()
    return parser.cards_list

if __name__ == "__main__":
    count = int(input("Сколько случайных карт проанализировать? "))
    all_cards = download_and_parse_cards(count)
    
    print("\n--- Результаты парсинга ---")
    for card in all_cards:
        print(f"Карта: {card.name} | Мана: {card.mana_cost} | P/T: {card.power_toughness}")

