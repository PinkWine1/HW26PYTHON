import logging
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler
from func import city_set,city_game,find_city_computer, loaded_cities


logger = logging.getLogger(__name__)


console_handler = logging.StreamHandler()

console_formatter = ColoredFormatter(
    fmt=(
        "%(asctime)s | "
        "%(log_color)s%(levelname)-8s%(reset)s | "
        "%(name)s | %(log_color)s%(message)s"
    ),
    datefmt="%H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "CRITICAL": "bold_white,bg_red",
    },
)

console_handler.setFormatter(console_formatter)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        console_handler,
        RotatingFileHandler("main.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    ]
)



def main() -> None:
    """
    Вход в программу. Управляет игрой
    """
    cities_list = loaded_cities()
    if cities_list is None:
        logger.critical("Игра не может быть запущена: Датасет городов недоступен")
        return
    available = city_set(cities_list)
    first_letters = {city[0] for city in available}
    last_letters = {city[-1] for city in available}
    bad_letters = last_letters - first_letters
    last_city = ""
    print("Игра в города!")
    print("Начинаем игру! Называй любой город и старайся не повторяться, а то проиграешь!")

    while True:
        user_input = input("Ваш город: ").strip().lower()
        logger.debug(f"Человек выбрал город: {user_input}")

        if user_input in ("стоп"):
            print("Вы завершили игру!")
            logger.info("Человек написал стоп, игра прекратилась")
            logger.info("Выход из игры")
            break

        if user_input not in available:
            print(
                f"Города {user_input} нет в списке или его уже использовали. Вы проиграли))"
            )
            logger.info("Компьютер выиграл человека, грустно...Восстание машин скоро...")
            logger.info("Выход из игры...")
            break
        if last_city and not city_game(last_city, user_input):
            print(f"Город должен начинаться на {last_city[-1]}. Вы проиграли((")
            logger.debug(f"Город должен начинаться на {last_city[-1]}")
            logger.info("Человек проиграл...")
            logger.info("Игра завершена...")
            break
        available.remove(user_input)
        last_city = user_input

        if last_city[-1] in bad_letters and len(last_city) > 1:
            needed_letter = last_city[-2]
        else:
            needed_letter = last_city[-1]
        computer_city = find_city_computer(available, needed_letter)
        if computer_city is None:
            logger.info("Человек выиграл робота, супер! Отменяем восстание машин!!!")
            print(
                f"Компьютер не может найти город на букву {needed_letter}. Мы выиграли, ес!)"
            )
            logger.info("Выход из игры...")
            break
        else:
            print(f"Компьютер выбрал {computer_city}")
            logger.debug(f"Компьютер выбрал город: {computer_city}")
            available.remove(computer_city)
            last_city = computer_city


main()