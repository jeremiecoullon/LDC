from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Player, Instrument

class InstrumentForm(ModelForm):

	class Meta:
		model = Instrument
		fields = ('name',)

class PlayerForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PlayerForm, self).__init__(*args, **kwargs)
		self.fields['external_URL'].help_text = "This can be a link to player's website, facebook, or whatever. This will be linked in the player's name in their information box."

	class Meta:
		model = Player
		fields = ('name', 'country', 'description', 'instrument', 'external_URL', 'image', 'isactive', 'band', 'festival', 'gigged_with', 'video_embed')
		widgets = {'instrument': FilteredSelectMultiple(verbose_name="instrument",
                                                      is_stacked=False,), 
					'gigged_with': FilteredSelectMultiple(verbose_name="gigged with",
			                                                      is_stacked=False,)
		}