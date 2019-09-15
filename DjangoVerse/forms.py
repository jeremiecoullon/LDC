from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Player, Instrument

class InstrumentForm(ModelForm):

	class Meta:
		model = Instrument
		fields = ('name',)

class PlayerForm(ModelForm):

	class Meta:
		model = Player
		fields = ('name', 'country', 'description', 'instrument', 'external_URL', 'image', 'isactive', 'band', 'festival', 'gigged_with')
		widgets = {'instrument': FilteredSelectMultiple(verbose_name="instrument",
                                                      is_stacked=False,), 
					'gigged_with': FilteredSelectMultiple(verbose_name="gigged with",
			                                                      is_stacked=False,)
		}