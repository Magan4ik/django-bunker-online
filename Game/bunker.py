
import random

from Game.dtos import GameDTO, PlayerDTO, BunkerDTO


def get_random_line(filename: str, index: int = None) -> str:
    with open(filename, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        if not index:
            index = random.randint(0, len(lines) - 1)
        return lines[index].strip()


class Bunker:
    sick_k = 0.4
    hobby_k = 0.15
    job_k = 0.1
    phobia_k = 0.4
    baggage_k = 0.2
    knowledge_k = 0.05
    food_k = 0.02
    rooms_k = 0.3

    files = {"sick": "data\\Болезни.txt",
             "hobby": {"<18": "data\\Хобби до 18.txt",
                       ">18": "data\\Хобби после 18.txt"},
             "phobia": "data\\Фобии.txt",
             "baggage": "data\\Багаж.txt",
             "quality": "data\\Качества.txt",
             "knowledge": "data\\Знание.txt",
             "job": {"<18": "data\\Работа до 18.txt",
                     ">18": "data\\Работа после 18.txt"},
             "time": "data\\Время.txt",
             "catastrophe": "data\\Катастрофы.txt",
             "rooms": "data\\Комнаты.txt",
             "seasons": "data\\Сезоны.txt",
             "locations": "data\\Локации.txt"}

    @classmethod
    def start(cls, amount: int):
        return GameDTO(info=cls.create_situation(amount),
                       players=[cls.create_player() for _ in range(amount)])

    @classmethod
    def create_player(cls):
        age = random.randint(14, 80)
        if age < 18:
            hobby_file = cls.files["hobby"]["<18"]
            job_file = cls.files["job"]["<18"]
        else:
            hobby_file = cls.files["hobby"][">18"]
            job_file = cls.files["job"][">18"]
        hobby = "Бездарь" if random.random() <= cls.hobby_k else get_random_line(hobby_file)
        job = "Трясе копійки з бабусі (безробітній)" if random.random() <= cls.job_k else get_random_line(job_file)

        return PlayerDTO(
            sex=random.choice(["Хлопчина", "Дівчинка"]),
            age=age,
            sick="Придатний (здоров)" if random.random() <= cls.sick_k else get_random_line(cls.files["sick"]),
            hobby=hobby,
            phobia="Безстрашний" if random.random() <= cls.phobia_k else get_random_line(cls.files["phobia"]),
            baggage="Порожняк" if random.random() <= cls.baggage_k else ', '.join(
                get_random_line(cls.files["baggage"]) for _ in range(random.randint(1, 2))
            ),
            quality=get_random_line(cls.files["quality"]),
            knowledge="Довбень" if random.random() <= cls.knowledge_k else ', '.join(
                get_random_line(cls.files["knowledge"]) for _ in range(random.randint(2, 3))
            ),
            job=job
        )

    @classmethod
    def create_situation(cls, amount: int):
        catastrophe = get_random_line(cls.files["catastrophe"])
        season = get_random_line(cls.files["seasons"])
        location = get_random_line(cls.files["locations"])
        room_sizes = ["Маленький", "Середній", "Великий"]
        room_size = room_sizes[min((amount // 5) - 1, 2)]
        rooms = "Немає" if random.random() <= cls.rooms_k else get_random_line(cls.files["rooms"])
        places = random.randint((amount // 2), (amount // 2) + 1)
        time, days = cls._generate_random_bunker_period()
        food = cls._generate_random_food_period(days)
        return BunkerDTO(
            catastrophe=catastrophe,
            season=season,
            location=location,
            room_size=room_size,
            rooms=rooms,
            places=places,
            time=time,
            food=food
        )

    @classmethod
    def _generate_random_bunker_period(cls):
        years = random.randint(0, 4)
        months = random.randint(0, 11)
        days = random.randint(0, 30)

        total_days = years * 365 + months * 30 + days
        if total_days < 500:
            total_days = 500

        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        period_str = f"{years} {cls._get_year_declension(years)} {months} {cls._get_month_declension(months)} {days} {cls._get_day_declension(days)}"

        return period_str, total_days

    @classmethod
    def _get_year_declension(cls, years):
        if 11 <= years % 100 <= 14:
            return "років"
        elif years % 10 == 1:
            return "рік"
        elif 2 <= years % 10 <= 4:
            return "роки"
        else:
            return "років"

    @classmethod
    def _get_month_declension(cls, months):
        if 11 <= months % 100 <= 14:
            return "місяців"
        elif months % 10 == 1:
            return "місяць"
        elif 2 <= months % 10 <= 4:
            return "місяці"
        else:
            return "місяців"

    @classmethod
    def _get_day_declension(cls, days):
        if 11 <= days % 100 <= 14:
            return "днів"
        elif days % 10 == 1:
            return "день"
        elif 2 <= days % 10 <= 4:
            return "дні"
        else:
            return "днів"

    @classmethod
    def _generate_random_food_period(cls, bunker_total_days):
        if random.random() < cls.food_k:
            food_total_days = bunker_total_days
        else:
            food_total_days = random.randint(90, bunker_total_days - 1)

        years = food_total_days // 365
        remaining_days = food_total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        food_period_str = f"{years} {cls._get_year_declension(years)} {months} {cls._get_month_declension(months)} {days} {cls._get_day_declension(days)}"

        return food_period_str


if __name__ == '__main__':
    print(Bunker.start(6))
