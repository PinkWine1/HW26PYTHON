import json
import logging
logger = logging.getLogger(__name__)

def loaded_cities(filename: str = "cities.json") -> list[dict] | None:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info("Игра успешно запущена после загрузки датасета!")
            return data
    except FileNotFoundError:
        logger.critical("Не найден файл с датасетом городов")
        return None
    except json.JSONDecodeError:
        logger.critical("Не удалось декодировать JSON с городами")
        return None



def city_set(cities_list: list[dict]) -> set[str]:
    """
    Добавляет города(их названия) из списка словарей и приводит их к нижнему регистру

    Arguments:
        cities_list: list[dict]:Список словарей по ключу 'name'
    Returns:
        set[str] - Множество названий городов
    """
    cities = set()
    for city in cities_list:
        cities.add(city["name"].lower())
    return cities


def city_game(city1: str, city2: str) -> bool:
    """
    Последняя буква city1 должна совпадать с первой буквой city2

    Arguments:
        city1:str - предыдущий город
        city2:str - следующий город
    Returns:
        bool: True, если все правильно, иначе false
    """
    if not city1 or not city2:
        return False
    return city1[-1].lower() == city2[0].lower()


def find_city_computer(available: set[str], letter: str) -> str | None:
    """
    Ищет в множестве город, начинающийся на нужную букву.

    Arguments:
        available:set[str] - Множество городов. которые еще не выбраны
        letter:str - буква, на которую должен начинаться город
    Returns: str | None - Найденный город | None, если город не найден
    """
    for city in available:
        if city[0] == letter:
            return city
    return None