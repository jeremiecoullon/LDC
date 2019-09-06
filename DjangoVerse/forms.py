from django.forms import ModelForm

from .models import Player, Instrument, Festival, Band

class InstrumentForm(ModelForm):

	class Meta:
		model = Instrument
		fields = ('name',)

class PlayerForm(ModelForm):

	class Meta:
		model = Player
		fields = ('name', 'country', 'description', 'instrument', 'external_URL', 'image', 'isactive', 'band', 'festival')


class FestivalForm(ModelForm):

	class Meta:
		model = Festival
		fields = ('name', 'country', 'description', 'external_URL', 'image', 'isactive')



class BandForm(ModelForm):

	class Meta:
		model = Band
		fields = ('name', 'country', 'description', 'external_URL', 'image', 'isactive')