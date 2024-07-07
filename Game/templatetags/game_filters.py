from django import template
from django.contrib.auth import get_user_model
from Game.models import Game, PlayerInfo

User = get_user_model()

register = template.Library()


@register.filter
def owner_nickname(game: Game) -> str:
    player = PlayerInfo.objects.filter(player_id=game.owner_id)
    if player.exists():
        return player.first().nickname
    return "Unknowing"

