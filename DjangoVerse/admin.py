from django.contrib import admin

from .models import Player, Band, Festival, Venue, Album, Instrument



@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	filter_horizontal = ('band', 'instrument', 'festival',)# 'venue', 'album',)

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
	filter_horizontal = ('festival', )#'venue', 'album',)

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
	pass

# @admin.register(Venue)
# class VenueAdmin(admin.ModelAdmin):
# 	pass

# @admin.register(Album)
# class AlbumAdmin(admin.ModelAdmin):
# 	pass

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	pass
