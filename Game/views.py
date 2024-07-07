import uuid

from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from Game.models import Game, PlayerInfo

from Game.facades import BunkerFacade


# Create your views here.


def main_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        nickname = request.POST.get('nickname')
        if not nickname:
            return redirect("Game:main")
        try:
            with transaction.atomic():
                game = Game.objects.create()
                player = BunkerFacade.create_player(game, nickname)
                game.owner_id = player.player_id
                game.save()
                request.session["game_id"] = str(game.game_id)
                request.session["player_id"] = str(player.player_id)
        except Exception as e:
            print(f"Error occurred: {e}")

        return redirect("Game:lobby", str(game.game_id))

    return render(request, 'game/main_page.html')


def lobby_view(request: HttpRequest, game_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    if request.method == "GET":
        player_id = request.session.get("player_id")

        request.session["game_id"] = game_id

        player = PlayerInfo.objects.filter(player_id=player_id, game__game_id=game_id)
        if not player.exists():
            if len(game.players.all()) < game.max_players and game.status == "open":
                nickname = request.GET.get("nickname")
                if not nickname:
                    return redirect("Game:main")
                player = BunkerFacade.create_player(game, nickname)
                request.session["player_id"] = str(player.player_id)
            else:
                return redirect("Game:main")
        else:
            player = player.first()

        return render(request, 'game/game_lobby.html', {'game': game, 'client': player})
    elif request.method == "POST":
        if (game.status == "open" or game.status == "closed") and request.session.get("player_id") == str(game.owner_id):
            game.status = "started"
            info = BunkerFacade.create_info(len(game.players.all()))
            game.info = info
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
        get_object_or_404(PlayerInfo, player_id=player_id).delete()
        return redirect("Game:main")
    return redirect("Game:lobby", game_id)


def kick_lobby_view(request: HttpRequest, game_id: str, player_id: str) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    player = get_object_or_404(PlayerInfo, player_id=player_id, game__game_id=game_id)
    if request.session.get("player_id") == str(game.owner_id):
        player.delete()
    return redirect("Game:lobby", game_id)


def game_list_view(request: HttpRequest) -> HttpResponse:
    games = Game.objects.filter(status="open")
    return render(request, 'game/game_list.html', {"games": games})


def bunker_view(request: HttpRequest, game_id: str) -> HttpResponse:
    player = get_object_or_404(PlayerInfo, player_id=request.session.get("player_id"), game__game_id=game_id)
    info = player.game.info
    return render(request, 'game/bunker_page.html', {"info": info, "player": player})


def game_status_check(request: HttpRequest, game_id: str) -> JsonResponse:
    game = Game.objects.filter(game_id=game_id)
    if game.exists():
        return JsonResponse({"status": game.first().status == "started"})
    else:
        return JsonResponse({"status": False})


def game_kick_check(request: HttpRequest, player_id: str) -> JsonResponse:
    player = PlayerInfo.objects.filter(player_id=player_id)
    return JsonResponse({"status": player.exists()})


def game_connect_check(request: HttpRequest, game_id: str, amount: int) -> JsonResponse:
    game = Game.objects.filter(game_id=game_id)
    return JsonResponse({"status": len(game.first().players.all()) != amount})


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

