import uuid

from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from Game.models import Game, PlayerInfo, Profile, PlayerCharacteristic

from Game.facades import BunkerFacade
from Game.bunker import Bunker


def bunker_view(request: HttpRequest, game_id: str) -> HttpResponse:
    profile = get_object_or_404(Profile, player_id=request.session.get("player_id"), game__game_id=game_id)
    game = profile.game
    return render(request, 'game/bunker_page.html', {"game": game, "player": profile.player_info})


def make_turn_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player_id = request.session.get("player_id")
    profile = get_object_or_404(Profile, player_id=player_id, game=game)
    if game.turn != profile.number:
        return redirect('Game:bunker', game_id)
    if request.GET.get('age'):
        profile.player_info.age.status = "opened"
        profile.player_info.age.save()
    if request.GET.get('sick'):
        profile.player_info.sick.status = "opened"
        profile.player_info.sick.save()
    if request.GET.get('hobby'):
        profile.player_info.hobby.status = "opened"
        profile.player_info.hobby.save()
    if request.GET.get('phobia'):
        profile.player_info.phobia.status = "opened"
        profile.player_info.phobia.save()
    if request.GET.get('baggage'):
        profile.player_info.baggage.status = "opened"
        profile.player_info.baggage.save()
    if request.GET.get('quality'):
        profile.player_info.quality.status = "opened"
        profile.player_info.quality.save()
    if request.GET.get('knowledge'):
        profile.player_info.knowledge.status = "opened"
        profile.player_info.knowledge.save()
    if request.GET.get('job'):
        profile.player_info.job.status = "opened"
        profile.player_info.job.save()
    profile.save()
    game.next_player()
    turn = game.turn
    while not Profile.objects.filter(number=turn, game=game).exists():
        game.next_player()
        turn = game.turn
    return redirect('Game:bunker', game_id)


def turn_check(request: HttpRequest, game_id: str, turn: int) -> JsonResponse:
    game = Game.objects.filter(game_id=game_id)
    return JsonResponse({"status": game.first().turn != turn})
