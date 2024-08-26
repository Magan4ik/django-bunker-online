import uuid
from typing import Optional
import random
from dataclasses import asdict

from django.db.models import QuerySet

from Game.models import PlayerInfo, PlayerCharacteristic, BunkerCharacteristic, BunkerInfo
from Game.bunker import PlayerDTO, BunkerDTO


class BunkerFacade:

    @classmethod
    def create_player_from_dto(cls, player_dto: PlayerDTO) -> PlayerInfo:
        return PlayerInfo.objects.create(
            sex=player_dto.sex,
            age=PlayerCharacteristic.objects.create(name=player_dto.age),
            sick=PlayerCharacteristic.objects.create(**asdict(player_dto.sick)),
            hobby=PlayerCharacteristic.objects.create(**asdict(player_dto.hobby)),
            phobia=PlayerCharacteristic.objects.create(**asdict(player_dto.phobia)),
            baggage=PlayerCharacteristic.objects.create(**asdict(player_dto.baggage)),
            quality=PlayerCharacteristic.objects.create(**asdict(player_dto.quality)),
            knowledge=PlayerCharacteristic.objects.create(**asdict(player_dto.knowledge)),
            job=PlayerCharacteristic.objects.create(**asdict(player_dto.job)),
        )

    @classmethod
    def create_info_from_dto(cls, info_dto: BunkerDTO) -> BunkerInfo:
        return BunkerInfo.objects.create(**asdict(info_dto))
