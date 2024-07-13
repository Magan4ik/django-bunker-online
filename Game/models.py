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
    STATUS_CHOICES = (
        ('hidden', 'Hidden'),
        ('opened', 'Opened')
    )

    value = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="hidden")

    def __str__(self):
        return f"{self.value} ({self.status})"


class BunkerInfo(models.Model):
    catastrophe = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    room_size = models.CharField(max_length=100)
    rooms = models.CharField(max_length=100)
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
    turn = models.PositiveIntegerField(default=1)

    def next_player(self):
        self.turn += 1
        if self.turn > self.max_players:
            self.turn = 1
        self.save()

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
    age = models.OneToOneField(PlayerCharacteristic, related_name="age_info", on_delete=models.CASCADE)
    sick = models.OneToOneField(PlayerCharacteristic, related_name="sick_info", on_delete=models.CASCADE)
    hobby = models.OneToOneField(PlayerCharacteristic, related_name="hobby_info", on_delete=models.CASCADE)
    phobia = models.OneToOneField(PlayerCharacteristic, related_name="phobia_info", on_delete=models.CASCADE)
    baggage = models.OneToOneField(PlayerCharacteristic, related_name="baggage_info", on_delete=models.CASCADE)
    quality = models.OneToOneField(PlayerCharacteristic, related_name="quality_info", on_delete=models.CASCADE)
    knowledge = models.OneToOneField(PlayerCharacteristic, related_name="knowledge_info", on_delete=models.CASCADE)
    job = models.OneToOneField(PlayerCharacteristic, related_name="job_info", on_delete=models.CASCADE)


class Profile(models.Model):
    nickname = models.CharField(max_length=12, default=generate_random_nickname)
    player_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, related_name="profiles", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    player_info = models.OneToOneField(PlayerInfo, related_name="profile", on_delete=models.CASCADE, null=True)
