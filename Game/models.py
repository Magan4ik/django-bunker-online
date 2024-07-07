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
    catastrophe = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    room_size = models.CharField(max_length=100)
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
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default="alive")
    sex = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    sick = models.CharField(max_length=100)
    hobby = models.CharField(max_length=100)
    phobia = models.CharField(max_length=100)
    baggage = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    knowledge = models.CharField(max_length=100)
    job = models.CharField(max_length=100)


class Profile(models.Model):
    nickname = models.CharField(max_length=12, default=generate_random_nickname)
    player_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, related_name="profiles", on_delete=models.CASCADE)
    player_info = models.OneToOneField(PlayerInfo, related_name="profile", on_delete=models.CASCADE, null=True)
