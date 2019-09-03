from django.contrib import admin
from .models import Player, Tune, Volume, Gig


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']
	exclude = ['slug']

@admin.register(Tune)
class TuneAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']


@admin.register(Gig)
class TuneAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']
