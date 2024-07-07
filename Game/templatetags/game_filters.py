from django import template
from django.contrib.auth import get_user_model
from Game.models import Game, Profile

User = get_user_model()

register = template.Library()


@register.filter
def owner_nickname(game: Game) -> str:
    profile = Profile.objects.filter(player_id=game.owner_id)
    if profile.exists():
        return profile.first().nickname
    return "Unknowing"

