import uuid

from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from Game.models import Game, PlayerInfo, Profile, PlayerCharacteristic

from Game.facades import BunkerFacade
from Game.bunker import Bunker


# Create your views here.


def lobby_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    if request.method == "GET":
        player_id = request.session.get("player_id")

        request.session["game_id"] = game_id

        profile = Profile.objects.filter(player_id=player_id, game__game_id=game_id)
        if not profile.exists():
            if len(game.profiles.all()) < game.max_players and game.status == "open":
                nickname = request.GET.get("nickname")
                profile = Profile.objects.create(game=game, nickname=nickname, number=len(game.profiles.all()) + 1)
                request.session["player_id"] = str(profile.player_id)
            else:
                return redirect("Game:main")
        else:
            profile = profile.first()

        return render(request, 'game/game_lobby.html', {'game': game, 'profile': profile})
    elif request.method == "POST":
        if (game.status == "open" or game.status == "closed") and request.session.get("player_id") == str(
                game.owner_id):
            game.status = "started"
            amount = len(game.profiles.all())
            game_info = Bunker.start(amount)
            info = BunkerFacade.create_info_from_dto(game_info.info)
            profiles = game.profiles.all()
            for profile, player in zip(profiles, game_info.players):
                player_info = BunkerFacade.create_player_from_dto(player)
                profile.player_info = player_info
                profile.save()
            game.info = info
            game.max_players = amount
            game.save()
            return redirect("Game:bunker", game_id)
        return redirect("Game:lobby", game_id)


def close_lobby_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player_id = request.session.get("player_id")
    if player_id == str(game.owner_id):
        game.status = "closed" if game.status == "open" else "open"
        game.save()
    return redirect("Game:lobby", game_id)


def delete_lobby_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player_id = request.session.get("player_id")
    if player_id == str(game.owner_id):
        game.delete()
        del request.session["player_id"]
        del request.session["game_id"]
        return redirect("Game:main")
    return redirect("Game:lobby", game_id)


def leave_lobby_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player_id = request.session.get("player_id")
    if player_id != str(game.owner_id):
        get_object_or_404(Profile, player_id=player_id).delete()
        return redirect("Game:main")
    return redirect("Game:lobby", game_id)


def kick_lobby_view(request: HttpRequest, game_id: str, player_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    profile = get_object_or_404(Profile, player_id=player_id, game__game_id=game_id)
    if request.session.get("player_id") == str(game.owner_id):
        profile.delete()
    return redirect("Game:lobby", game_id)


def game_status_check(request: HttpRequest, game_id: str) -> JsonResponse:
    game = Game.objects.filter(game_id=game_id)
    if game.exists():
        return JsonResponse({"status": game.first().status == "started"})
    else:
        return JsonResponse({"status": False})


def game_kick_check(request: HttpRequest, player_id: str) -> JsonResponse:
    profile = Profile.objects.filter(player_id=player_id)
    return JsonResponse({"status": profile.exists()})


def game_connect_check(request: HttpRequest, game_id: str, amount: int) -> JsonResponse:
    game = Game.objects.filter(game_id=game_id)
    return JsonResponse({"status": len(game.first().profiles.all()) != amount})


def plus_players_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player_id = request.session.get("player_id")
    if player_id == str(game.owner_id):
        game.max_players += 1
        game.save()
    return redirect("Game:lobby", game_id)


def minus_players_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player_id = request.session.get("player_id")
    if player_id == str(game.owner_id):
        game.max_players -= 1
        game.save()
    return redirect("Game:lobby", game_id)
