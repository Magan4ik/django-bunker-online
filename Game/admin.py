from django.contrib import admin
from Game.models import BunkerCharacteristic, PlayerCharacteristic, BunkerInfo, Game, PlayerInfo


@admin.register(BunkerCharacteristic)
class BunkerCharacteristicAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key', 'value')
    list_filter = ('key',)


@admin.register(PlayerCharacteristic)
class PlayerCharacteristicAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'type')
    search_fields = ('key', 'value')
    list_filter = ('key', 'type')


@admin.register(BunkerInfo)
class BunkerInfoAdmin(admin.ModelAdmin):
    list_display = ('catastrophe', 'season', 'location', 'room_size', 'places', 'time', 'food')
    search_fields = ('season', 'room_size')
    list_filter = ('season', 'room_size')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'owner_id', 'status', 'info')
    search_fields = ('game_id', 'status')
    list_filter = ('status',)


@admin.register(PlayerInfo)
class PlayerInfoAdmin(admin.ModelAdmin):
    list_display = ('sex', 'age')
    search_fields = ('sex', 'age', 'sick', 'hobby', 'phobia', 'baggage', 'quality', 'knowledge', 'job')
    list_filter = ('sex', 'status', 'age')
