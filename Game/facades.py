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
        return PlayerInfo.objects.create(**asdict(player_dto))

    @classmethod
    def create_info_from_dto(cls, info_dto: BunkerDTO) -> BunkerInfo:
        return BunkerInfo.objects.create(**asdict(info_dto))
