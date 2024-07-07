from django.urls import path
from Game import views

app_name = "Game"

urlpatterns = [
    path('', views.main_view, name="main"),
    path('games/', views.game_list_view, name="games"),
    path('lobby/<str:game_id>/', views.lobby_view, name="lobby"),
    path('lobby/<str:game_id>/close', views.close_lobby_view, name="close_lobby"),
    path('lobby/<str:game_id>/delete', views.delete_lobby_view, name="delete_lobby"),
    path('lobby/<str:game_id>/leave', views.leave_lobby_view, name="leave_lobby"),
    path('lobby/<str:game_id>/kick/<str:player_id>/', views.kick_lobby_view, name="kick_lobby"),
    path('lobby/<str:game_id>/statuscheck/', views.game_status_check, name="status_check"),
    path('lobby/<str:player_id>/kickcheck/', views.game_kick_check, name="kick_check"),
    path('lobby/<str:game_id>/checkconnect/<int:amount>/', views.game_connect_check, name="connect_check"),
    path('lobby/<str:game_id>/plus/', views.plus_players_view, name="lobby_plus"),
    path('lobby/<str:game_id>/minus/', views.minus_players_view, name="lobby_minus"),
    path('bunker/<str:game_id>/', views.bunker_view, name="bunker"),
]