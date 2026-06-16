import re
from datetime import date

def normalize_title(title: str) -> str:
    title = title.lower().strip()

    title = re.sub(r"[™®©]", "", title)
    title = re.sub(
        r'(\s*-\s*)?(game of the year|deluxe|goty|complete edition|ultimate edition|dlc|bundle|pack).*',
        '',
        title
    )

    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title)

    return title.strip()

GENRE_MAP = {
    # GabeStore
    "экшен": "Экшены",
    "приключения": "Приключения",
    "ролевые": "РПГ",
    "симуляторы": "Симуляторы",
    "стратегии": "Стратегии",
    "спортивные": "Спорт",
    "гонки": "Гонки",
    "казуальные": "Казуальные",
    "казуальные игры": "Казуальные",


    # SteamBuy
    "шутер": "Экшены",
    "файтинги": "Файтинги",
    "приключение": "Приключения",
    "симулятор": "Симуляторы",
    "ролевая игра": "РПГ",
    "спортивная игра": "Спорт",
    "казуальная игра": "Казуальные",
    "аниме": "Аниме",

    # Пропуски
    "онлайн": None,
    "подписка": None,
    "карта оплаты": None,
    "mmo": None,
    "классика": None,
    "жанры": None,
    "бесплатные": None,
    "приключенческие игры": "Приключения",
    "ранний доступ": None
}

def normalize_genres(genres):
    result = []

    for genre in genres:
        g_norm = genre.strip().lower()

        mapped = GENRE_MAP.get(g_norm)

        if mapped is None:
            continue

        result.append(mapped)

    if not result:
        result = ["Казуальные"]

    return sorted(set(result))

MONTHS = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4, "мая": 5, "июн": 6,
    "июл": 7, "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12
}

# "21 авг. 2012 г."  либо ISO "2026-06-05" (SteamBuy отдаёт ISO)
def normalize_date(ru_date: str) -> date | None:
    if not ru_date:
        return None

    # ISO YYYY-MM-DD (SteamBuy). "0000-00-00" и прочий мусор отсеются ValueError'ом.
    iso = re.fullmatch(r"\s*(\d{4})-(\d{2})-(\d{2})\s*", ru_date)
    if iso:
        try:
            return date(int(iso[1]), int(iso[2]), int(iso[3]))
        except ValueError:
            return None

    ru_date = ru_date.lower()

    # если дата не объявлена
    if "объяв" in ru_date or "скоро" in ru_date:
        return None

    ru_date = ru_date.replace('. ', ' ').replace('г.', '').strip()
    parts = ru_date.split()

    if len(parts) != 3:
        return None

    day, month, year = parts

    if not day.isdigit() or not year.isdigit():
        return None

    # MONTHS — 3-буквенные ключи. Steam даёт "авг.", gabestore — "февраля";
    # обрезка до 3 букв нормализует оба варианта ("фев", "авг", "мая"...).
    month_num = MONTHS.get(month[:3])
    if not month_num:
        return None

    return date(int(year), month_num, int(day))

def price_to_int(price: str) -> int:
    if price in ['Бесплатно', '', None]:
        return 0
    # Steam (RU) отдаёт "1 439,10₽": запятая — копейки, пробел — разряды тысяч.
    # Отбрасываем дробную часть (по , или .), затем чистим неразрядные символы.
    # Иначе \D-чистка склеила бы копейки с рублями: "1 439,10" → 143910.
    integer_part = re.split(r'[.,]', price)[0]
    digits = re.sub(r'\D', '', integer_part)
    return int(digits) if digits else 0
