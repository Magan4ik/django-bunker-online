from django.urls import path
from Game.views import game_views, lobby_views, general_views

app_name = "Game"

urlpatterns = [
    path('', general_views.main_view, name="main"),
    path('games/', general_views.game_list_view, name="games"),
    path('lobby/<str:game_id>/', lobby_views.lobby_view, name="lobby"),
    path('lobby/<str:game_id>/close', lobby_views.close_lobby_view, name="close_lobby"),
    path('lobby/<str:game_id>/delete', lobby_views.delete_lobby_view, name="delete_lobby"),
    path('lobby/<str:game_id>/leave', lobby_views.leave_lobby_view, name="leave_lobby"),
    path('lobby/<str:game_id>/kick/<str:player_id>/', lobby_views.kick_lobby_view, name="kick_lobby"),
    path('lobby/<str:game_id>/statuscheck/', lobby_views.game_status_check, name="status_check"),
    path('lobby/<str:player_id>/kickcheck/', lobby_views.game_kick_check, name="kick_check"),
    path('lobby/<str:game_id>/checkconnect/<int:amount>/', lobby_views.game_connect_check, name="connect_check"),
    path('lobby/<str:game_id>/plus/', lobby_views.plus_players_view, name="lobby_plus"),
    path('lobby/<str:game_id>/minus/', lobby_views.minus_players_view, name="lobby_minus"),
    path('bunker/<str:game_id>/', game_views.bunker_view, name="bunker"),
    path('bunker/<str:game_id>/maketurn', game_views.make_turn_view, name="make_turn"),
    path('bunker/<str:game_id>/turncheck/<int:turn>/', game_views.turn_check, name="turn_check"),
]