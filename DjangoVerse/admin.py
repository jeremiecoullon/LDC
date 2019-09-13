from django.contrib import admin

from .models import Player, Band, Festival, Venue, Album, Instrument



@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	filter_horizontal = ('band', 'instrument', 'festival',)# 'venue', 'album',)
	exclude = ('thumbnail', 'band', 'festival')
	# fk_name = 'from_player'
	filter_horizontal = ('gigged_with', 'instrument')

# @admin.register(Band)
# class BandAdmin(admin.ModelAdmin):
# 	filter_horizontal = ('festival', )#'venue', 'album',)
# 	exclude = ('thumbnail',)

# @admin.register(Festival)
# class FestivalAdmin(admin.ModelAdmin):
# 	exclude = ('thumbnail',)

# @admin.register(Venue)
# class VenueAdmin(admin.ModelAdmin):
# 	exclude = ('thumbnail',)

# @admin.register(Album)
# class AlbumAdmin(admin.ModelAdmin):
# 	exclude = ('thumbnail',)

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
	pass
