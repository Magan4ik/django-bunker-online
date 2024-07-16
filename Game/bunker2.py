import random

from Game.dtos import GameDTO, PlayerDTO, BunkerDTO, CharTypeDTO
import json


def convert_data():
    data_path = 'data/bunker_data.json'
    test_path = 'data/test_data.json'
    with open(data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        skill_data = dict()
        for skill in data["skills"]:
            skill_data[skill] = {"hobbies": list(),
                                 "baggage": list(),
                                 "knowledge": list(),
                                 "qualities": list(),
                                 "job<18": list(),
                                 "job>18": list(),
                                 "phobias": list(),
                                 "rooms": list(),
                                 "seasons": list(),
                                 "locations": list()}
        del data["skills"]
        del data["sick"]
        del data["catastrophes"]
        for key in data:
            for item in data[key]:
                bonus = item.get("bonus", [])
                for b in bonus:
                    skill_data[b][key].append(item)

    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump(skill_data, file)

    return skill_data


class Bunker:
    ran_k = {"sick": (.4, {"name": "Придатний (здоров)", "difficulty": 0, "provision": 0}),
             "hobbies": (.15, {"name": "Бездарь", "bonus": list()}),
             "baggage": (.2, {"name": "Порожняк", "bonus": list(), "provision": 0}),
             "knowledge": (.05, {"name": "Довбень", "bonus": list(), "provision": 0}),
             "qualities": (0,),
             "job<18": (.1, {"name": "На шиї у матусі (безробітній)", "bonus": list()}),
             "job>18": (.1, {"name": "Трясе копійки з бабусі (безробітній)", "bonus": list()}),
             "phobias": (.25, {"name": "Безстрашний", "provision": 0}),
             "food": (.07,)
             }

    wr_k = 0.7

    def __init__(self):
        self.info = None
        self.players = list()
        self.skill_data = convert_data()
        data_path = 'data/bunker_data.json'
        with open(data_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def _get_random_item(self, key: str):
        return random.choice(self.data[key])

    def start(self, amount: int):
        info = self.create_info(amount)
        self.info = info
        low_skills = [(skill, info.skill_data[skill]) for skill in info.skill_data if info.skill_data[skill] < 0]
        low_skills = dict(low_skills)
        characteristics = self.create_characteristics(low_skills, amount)
        sexes = ["Жіночка", "Жіночка", "Хлопчина", "Хлопчина"] + [random.choice(["Хлопчина", "Жіночка"])
                                                                  for _ in range(amount - 4)]
        random.shuffle(sexes)
        for i in range(amount):
            age = random.randint(14, 80)
            sick = characteristics["sick"][i]
            hobby = characteristics["hobbies"][i]
            phobia = characteristics["phobias"][i]
            knowledge = characteristics["knowledge"][i]
            job = characteristics["job>18"][i]
            baggage = characteristics["baggage"][i]
            quality = characteristics["qualities"][i]
            self.players.append(PlayerDTO(
                sex=sexes.pop(),
                age=age,
                sick=CharTypeDTO(name=sick["name"],
                                 difficulty=sick["difficulty"],
                                 provision=sick["provision"]),
                hobby=CharTypeDTO(name=hobby["name"], bonus=hobby["bonus"]),
                phobia=CharTypeDTO(name=phobia["name"], provision=phobia["provision"]),
                baggage=CharTypeDTO(name=baggage["name"], bonus=baggage["bonus"], provision=baggage["provision"]),
                quality=CharTypeDTO(name=quality["name"], provision=quality["provision"]),
                knowledge=CharTypeDTO(name=knowledge["name"], bonus=knowledge["bonus"],
                                      provision=knowledge["provision"]),
                job=CharTypeDTO(name=job["name"], bonus=job["bonus"])
            ))
        return GameDTO(
            info=self.info,
            players=self.players
        )

    def create_characteristics(self, low_skills: dict[str, int], amount: int):
        characteristics = {"sick": list(),
                           "hobbies": list(),
                           "baggage": list(),
                           "knowledge": list(),
                           "qualities": list(),
                           "job<18": list(),
                           "job>18": list(),
                           "phobias": list()
                           }
        for skill in low_skills:
            for i in range(abs(low_skills[skill])):
                key = random.choice(["hobbies", "baggage", "knowledge", "job>18"])
                while len(characteristics[key]) >= amount:
                    key = random.choice(["hobbies", "baggage", "knowledge", "job>18"])
                char = random.choice(self.skill_data[skill][key])
                characteristics[key].append(char)

        for char in characteristics:
            while len(characteristics[char]) < amount:
                c = self.ran_k[char][1] if random.random() <= self.ran_k[char][0] else self._get_random_item(char)
                characteristics[char].append(c)
            random.shuffle(characteristics[char])

        return characteristics

    def create_info(self, amount: int) -> BunkerDTO:
        bonuses = list()
        penalties = list()
        catastrophe = self._get_random_item(key="catastrophes")
        location = self._get_random_item(key="locations")
        season = self._get_random_item(key="seasons")
        season_type = random.choice(season["types"])
        rooms = [self._get_random_item(key="rooms") for _ in range(random.randint(1, 4))]
        bonuses += location["bonus"]
        bonuses += season["bonus"]
        bonuses += season_type["bonus"]
        penalties += catastrophe["penalty"]
        penalties += location["penalty"]
        penalties += season["penalty"]
        penalties += season_type["penalty"]
        for room in rooms:
            bonuses += room["bonus"]
        places = random.randint(round(amount / 2), round(amount / 2) + 1)

        time = random.randint(15, 60)
        food = round(time * 0.7, 1) if random.random() <= self.ran_k["food"][0] else random.randint(14, time)

        skill_data = dict()
        for skill in self.data["skills"]:
            skill_score = bonuses.count(skill) - penalties.count(skill)
            skill_data[skill] = skill_score

        win_req = sum([i for i in skill_data.values() if i < 0])

        info = BunkerDTO(catastrophe=catastrophe["name"],
                         season=season["name"],
                         season_type=season_type["name"] + ". " + season_type["description"],
                         location=location["name"],
                         rooms=' + '.join([room["name"] for room in rooms]),
                         places=places,
                         time=time,
                         timeout=catastrophe["timeout"],
                         food=food,
                         skill_data=skill_data,
                         win_req=win_req)

        return info


if __name__ == "__main__":
    bunker = Bunker()
    bunker.start(5)
    print(bunker.info)
    for p in bunker.players:
        print(p)
