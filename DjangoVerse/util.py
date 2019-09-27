import random
import string
from .models import Player, Instrument
from django.shortcuts import get_object_or_404

def randomString(stringLength=10):
    """
    Generate a random string of fixed length
    Use this to create random names
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_player(name, country, instrument, isactive):
	"""
	Function to automatically create a player. 
	Use this to test frontend: how many players can D3 handle before lagging too much
	"""
	
	leplayer = Player.objects.create(name=name, country=country, isactive=isactive)
	leplayer.save()
	# add gigged_with other players. 
	num_other_player = random.choice(range(2,20)) # choose random number of gigged_with
	for other_player in random.choices(list(Player.objects.all()), k=num_other_player): 
		leplayer.gigged_with.add(other_player)

	leinstrument = get_object_or_404(Instrument, name=instrument)
	leplayer.instrument.add(leinstrument)
	return leplayer
	

def create_many_players(num_players):
	list_countries = ['GB', 'FR', 'NL', 'US', 'DE']
	for elem in range(num_players):
		create_player(name=randomString(6), country=random.choice(list_countries), instrument='Guitar', isactive=True)


def delete_many_players(num_players):
	for other_player in Player.objects.all()[:num_players]: 
		other_player.delete()