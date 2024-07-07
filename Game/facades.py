import uuid
from typing import Optional
import random

from django.db.models import QuerySet

from Game.models import PlayerInfo, PlayerCharacteristic, BunkerCharacteristic, BunkerInfo


class BunkerFacade:
    sick_k = 0.25
    hobby_k = 0.15
    job_k = 0.1
    phobia_k = 0.2
    baggage_k = 0.2
    knowledge_k = 0.05

    @classmethod
    def create_player(cls, game, nickname: str = None) -> PlayerInfo:
        return PlayerInfo.objects.create(
            nickname=nickname,
            game=game,
            sex=random.choice(["male", "female"]),
            age=random.randint(14, 80),
            sick=PlayerCharacteristic.get_random("sick"),
            hobby=PlayerCharacteristic.get_random("hobby"),
            phobia=PlayerCharacteristic.get_random("phobia"),
            baggage=PlayerCharacteristic.get_random("baggage"),
            quality=PlayerCharacteristic.get_random("quality"),
            knowledge=PlayerCharacteristic.get_random("knowledge"),
            job=PlayerCharacteristic.get_random("job")
        )

    @classmethod
    def create_info(cls, amount: int) -> BunkerInfo:
        time, days = cls._generate_random_bunker_period()
        food = cls._generate_random_food_period(days)
        return BunkerInfo.objects.create(
            catastrophe=BunkerCharacteristic.objects.filter(key="catastrophe").order_by("?").first(),
            season=random.choice(["summer", "autumn", "spring", "winter"]),
            location=BunkerCharacteristic.objects.filter(key="locations").order_by("?").first(),
            room_size=random.choice(["small", "medium", "large"]),
            places=random.randint((amount // 2), (amount // 2) + 1),
            time=time,
            food=food
        )

    @classmethod
    def _generate_random_bunker_period(cls):
        years = random.randint(0, 2)
        months = random.randint(0, 11)
        days = random.randint(0, 30)

        total_days = years * 365 + months * 30 + days
        if total_days < 90:
            total_days = 90

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
        if random.random() < 0.6:
            food_total_days = bunker_total_days
        else:
            food_total_days = random.randint(90, bunker_total_days - 1)

        years = food_total_days // 365
        remaining_days = food_total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        food_period_str = f"{years} {cls._get_year_declension(years)} {months} {cls._get_month_declension(months)} {days} {cls._get_day_declension(days)}"

        return food_period_str
