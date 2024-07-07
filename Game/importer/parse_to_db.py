import django
import os

from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from Game.models import PlayerCharacteristic, BunkerCharacteristic

files = {"sick": "data/Болезни.txt",
         "hobby": {"<18": "data/Хобби до 18.txt",
                   ">18": "data/Хобби после 18.txt"},
         "phobia": "data/Фобии.txt",
         "baggage": "data/Багаж.txt",
         "quality": "data/Качества.txt",
         "knowledge": "data/Знание.txt",
         "job": {"<18": "data/Работа до 18.txt",
                 ">18": "data/Работа после 18.txt"},
         "time": "data/Время.txt",
         "catastrophe": "data/Катастрофы.txt",
         "rooms": "data/Комнаты.txt",
         "seasons": "data/Сезоны.txt",
         "locations": "data/Локации.txt"}


def get_lines(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(lambda x: x.strip(), list(file.readlines())))


@transaction.atomic
def load_to_db():

    for key in files:
        if key not in ["time", "food", "seasons", "rooms"]:
            if key not in ["job", "hobby"]:
                lines = get_lines(files[key])
            else:
                lines = get_lines(files[key]["<18"]) + get_lines(files[key][">18"])
            for line in lines:
                try:
                    if key in ["catastrophe", "locations"]:
                        BunkerCharacteristic.objects.create(key=key, value=line)
                    else:
                        PlayerCharacteristic.objects.create(key=key, value=line, type="random")
                except Exception as exp:
                    print(key, line, exp)


if __name__ == '__main__':
    load_to_db()
