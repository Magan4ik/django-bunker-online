import uuid

from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from Game.models import Game, PlayerInfo, Profile, PlayerCharacteristic

from Game.facades import BunkerFacade
from Game.bunker import Bunker


def main_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        nickname = request.POST.get('nickname')
        if not nickname:
            return redirect("Game:main")
        try:
            with transaction.atomic():
                game = Game.objects.create()
                profile = Profile.objects.create(game=game, nickname=nickname, number=1)
                game.owner_id = profile.player_id
                game.save()
                request.session["game_id"] = str(game.game_id)
                request.session["player_id"] = str(profile.player_id)
        except Exception as e:
            print(f"Error occurred: {e}")

        return redirect("Game:lobby", str(game.game_id))

    return render(request, 'game/main_page.html')


def game_list_view(request: HttpRequest) -> HttpResponse:
    games = Game.objects.filter(status="open")
    return render(request, 'game/game_list.html', {"games": games})
