from django.contrib import admin
from .models import Player, Tune, Volume


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	pass
