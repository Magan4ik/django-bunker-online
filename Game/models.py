import random
import string
import uuid
from typing import Optional

from django.db import models
from django.utils import timezone


# Create your models here.

def generate_random_nickname(length=8):
    random_number = ''.join(random.choices(string.digits, k=4))
    random_string = ''.join(random.choices(string.ascii_letters, k=length))
    return f"SomeUser{random_string}{random_number}"


class BunkerCharacteristic(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key}: {self.value}"


class PlayerCharacteristic(models.Model):
    char_k = {"sick": 0.25,
              "hobby": 0.15,
              "job": 0.1,
              "phobia": 0.2,
              "baggage": 0.2,
              "knowledge": 0.05}

    TYPE_CHOICE = (
        ("default", "Default"),
        ("random", "Random")
    )
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=TYPE_CHOICE, default="random")

    @classmethod
    def get_random(cls, key: str) -> Optional[models.Model]:
        k = cls.char_k.get(key, 0)
        qs = PlayerCharacteristic.objects.filter(key=key)
        if qs.exists():
            if random.random() > k:
                char = qs.filter(type="random").order_by("?").first()
            else:
                char = qs.filter(type="default").first()
            return char

    def __str__(self):
        return f"{self.key}: {self.value}"


class BunkerInfo(models.Model):
    SEASON_CHOICE = (
        ("summer", "Літо"),
        ("spring", "Весна"),
        ("autumn", "Осінь"),
        ("winter", "Зима")
    )
    ROOM_CHOICE = (
        ("small", "Маленький"),
        ("medium", "Середній"),
        ("large", "Великий"),
    )
    catastrophe = models.ForeignKey(BunkerCharacteristic, related_name="catastrophe_games",
                                    on_delete=models.SET_NULL, null=True)
    season = models.CharField(max_length=200, choices=SEASON_CHOICE)
    location = models.ForeignKey(BunkerCharacteristic, related_name="location_games",
                                 on_delete=models.SET_NULL, null=True)
    room_size = models.CharField(max_length=100, choices=ROOM_CHOICE)
    places = models.PositiveIntegerField()
    time = models.CharField(max_length=100)
    food = models.CharField(max_length=100)


class Game(models.Model):
    STATUS_CHOICE = (
        ("started", "Почата"),
        ("finished", "Закінчена"),
        ("open", "Лобі відкрите"),
        ("closed", "Лобі закрите"),
        ("cancelled", "Скасована"),
    )
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_id = models.UUIDField(null=True)
    max_players = models.PositiveIntegerField(default=5)
    status = models.CharField(choices=STATUS_CHOICE, max_length=16, default="open")
    info = models.ForeignKey(BunkerInfo, related_name="games", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.status == "started" and self.started_at is None:
            self.started_at = timezone.now()
        if self.status == "finished" and self.finished_at is None:
            self.finished_at = timezone.now()
        super().save(*args, **kwargs)


class PlayerInfo(models.Model):
    STATUS_CHOICE = (
        ("dead", "Мертв"),
        ("alive", "Живий"),
        ("winner", "Переможець")
    )
    SEX_CHOICE = (
        ("male", "Хлопчина"),
        ("female", "Жіночка")
    )
    nickname = models.CharField(max_length=12, default=generate_random_nickname)
    player_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, related_name="players", on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default="alive")
    sex = models.CharField(max_length=10, choices=SEX_CHOICE)
    age = models.PositiveIntegerField()
    sick = models.ForeignKey(PlayerCharacteristic, related_name="sick_games", on_delete=models.SET_NULL, null=True)
    hobby = models.ForeignKey(PlayerCharacteristic, related_name="hobby_games", on_delete=models.SET_NULL, null=True)
    phobia = models.ForeignKey(PlayerCharacteristic, related_name="phobia_games", on_delete=models.SET_NULL, null=True)
    baggage = models.ForeignKey(PlayerCharacteristic, related_name="baggage_games", on_delete=models.SET_NULL, null=True)
    quality = models.ForeignKey(PlayerCharacteristic, related_name="quality_games", on_delete=models.SET_NULL, null=True)
    knowledge = models.ForeignKey(PlayerCharacteristic, related_name="knowledge_games", on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(PlayerCharacteristic, related_name="job_games", on_delete=models.SET_NULL, null=True)
