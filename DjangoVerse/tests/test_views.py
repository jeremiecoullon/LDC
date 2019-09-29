from django.test import TestCase
from DjangoVerse.views import filter_nodes
from DjangoVerse.models import Player, Instrument, Band, Festival, Venue, Album

def create_player(name, country, instrument, isactive):
	leplayer = Player.objects.create(name=name, country=country, isactive=isactive)
	leplayer.save()
	leinstrument = Instrument.objects.create(name=instrument)
	leplayer.instrument.add(leinstrument)
	return leplayer

def create_band(name, country, isactive):
	leband = Band.objects.create(name=name, country=country, isactive=isactive)
	leband.save()
	return leband

def create_festival(name, country, isactive):
	lefesival = Festival.objects.create(name=name, country=country, isactive=isactive)
	lefesival.save()
	return lefesival

def create_album(name, country):
	lealbum = Album.objects.create(name=name, country=country)
	lealbum.save()
	return lealbum

def create_venue(name, country, isactive):
	levenue = Venue.objects.create(name=name, country=country, isactive=isactive)
	levenue.save()
	return levenue

class ARequest:
	"""
	Class with "query_params" dictionary attribute to simulate a request
	"""

	def __init__(self, **kwargs):
		self.query_params = kwargs



class TestFilterFunction(TestCase):

	def test_filter_nodes_player(self):
		leplayer1 = create_player(name='Bob', country='UK', instrument='Guitar', isactive=True)
		leplayer2 = create_player(name='Francois', country='France', instrument='Guitar', isactive=True)
		# leband1 =  create_band(name='Hot Club of Gypsy Jazz', country='USA', isactive=True)
		# leband2 =  create_band(name='A fun band', country='USA', isactive=False)
		# lefestival1 = create_festival(name='Samois', country='France', isactive=True)
		# lefestival2 = create_festival(name='IGGF', country='UK', isactive=False)
		# lealbum = create_album(name='le first album', country='Norway')
		# lealbum = create_album(name='le second album', country='Italy')
		# levenue = create_venue(name='a fun venue', country='Norway', isactive=True)
		# levenue = create_venue(name='another fun venue', country='Italy', isactive=False)

		request = ARequest(player_country='UK', player='on')
		model_dict = filter_nodes(request)
		self.assertQuerysetEqual(model_dict['player']['qs'], ["<Player: Bob>"])
		self.assertEqual(list(model_dict.keys()), ['player'])

		request = ARequest(player_country='France', player='on')
		model_dict = filter_nodes(request)
		self.assertQuerysetEqual(model_dict['player']['qs'], ["<Player: Francois>"])
		self.assertEqual(list(model_dict.keys()), ['player'])

	# def test_filter_nodes_band(self):
	# 	leplayer1 = create_player(name='Bob', country='UK', instrument='Guitar', isactive=True)
	# 	leplayer2 = create_player(name='Francois', country='France', instrument='Guitar', isactive=True)
	# 	leband1 =  create_band(name='Hot Club of Gypsy Jazz', country='USA', isactive=True)
	# 	leband2 =  create_band(name='A fun band', country='USA', isactive=False)
	# 	lefestival1 = create_festival(name='Samois', country='France', isactive=True)
	# 	lefestival2 = create_festival(name='IGGF', country='UK', isactive=False)
	# 	lealbum = create_album(name='le first album', country='Norway')
	# 	lealbum = create_album(name='le second album', country='Italy')
	# 	levenue = create_venue(name='a fun venue', country='Norway', isactive=True)
	# 	levenue = create_venue(name='another fun venue', country='Italy', isactive=False)

	# 	request = ARequest(band_country='France', band='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(model_dict['band']['qs'], [])
	# 	self.assertEqual(list(model_dict.keys()), ['band'])

	# 	# both active and non active bands
	# 	request = ARequest(band_country='USA', band='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['band']['qs']), ["<Band: Hot Club of Gypsy Jazz>", "<Band: A fun band>"])
	# 	self.assertEqual(list(model_dict.keys()), ['band'])

	# 	# only active bands
	# 	request = ARequest(band_country='USA', band='on', active=True)
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(model_dict['band']['qs'], ["<Band: Hot Club of Gypsy Jazz>"])
	# 	self.assertEqual(list(model_dict.keys()), ['band'])


	# def test_filter_nodes_festival(self):
	# 	leplayer1 = create_player(name='Bob', country='UK', instrument='Guitar', isactive=True)
	# 	leplayer2 = create_player(name='Francois', country='France', instrument='Guitar', isactive=True)
	# 	leband1 =  create_band(name='Hot Club of Gypsy Jazz', country='USA', isactive=True)
	# 	leband2 =  create_band(name='A fun band', country='USA', isactive=False)
	# 	lefestival1 = create_festival(name='Samois', country='France', isactive=True)
	# 	lefestival2 = create_festival(name='IGGF', country='UK', isactive=False)
	# 	lealbum = create_album(name='le first album', country='Norway')
	# 	lealbum = create_album(name='le second album', country='Italy')
	# 	levenue = create_venue(name='a fun venue', country='Norway', isactive=True)
	# 	levenue = create_venue(name='another fun venue', country='Italy', isactive=False)

	# 	request = ARequest(festival_country='France', festival='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(model_dict['festival']['qs'], ["<Festival: Samois>"])
	# 	self.assertEqual(list(model_dict.keys()), ['festival'])

	# 	# both active and non active festival
	# 	request = ARequest(festival='on',)
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['festival']['qs']), ["<Festival: Samois>", "<Festival: IGGF>"])
	# 	self.assertEqual(list(model_dict.keys()), ['festival'])

	# 	# only active festivals
	# 	request = ARequest(festival='on', active=True)
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['festival']['qs']), ["<Festival: Samois>"])
	# 	self.assertEqual(list(model_dict.keys()), ['festival'])


	# def test_filter_nodes_album(self):
	# 	leplayer1 = create_player(name='Bob', country='UK', instrument='Guitar', isactive=True)
	# 	leplayer2 = create_player(name='Francois', country='France', instrument='Guitar', isactive=True)
	# 	leband1 =  create_band(name='Hot Club of Gypsy Jazz', country='USA', isactive=True)
	# 	leband2 =  create_band(name='A fun band', country='USA', isactive=False)
	# 	lefestival1 = create_festival(name='Samois', country='France', isactive=True)
	# 	lefestival2 = create_festival(name='IGGF', country='UK', isactive=False)
	# 	lealbum = create_album(name='le first album', country='Norway')
	# 	lealbum = create_album(name='le second album', country='Italy')
	# 	levenue = create_venue(name='a fun venue', country='Norway', isactive=True)
	# 	levenue = create_venue(name='another fun venue', country='Italy', isactive=False)

	# 	request = ARequest(album_country='France', album='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(model_dict['album']['qs'], [])
	# 	self.assertEqual(list(model_dict.keys()), ['album'])

	# 	request = ARequest(album='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['album']['qs']), ["<Album: le first album>", "<Album: le second album>"])
	# 	self.assertEqual(list(model_dict.keys()), ['album'])

	# 	request = ARequest(album='on', album_country="Italy")
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['album']['qs']), ["<Album: le second album>"])
	# 	self.assertEqual(list(model_dict.keys()), ['album'])



	# def test_filter_nodes_venue(self):
	# 	leplayer1 = create_player(name='Bob', country='UK', instrument='Guitar', isactive=True)
	# 	leplayer2 = create_player(name='Francois', country='France', instrument='Guitar', isactive=True)
	# 	leband1 =  create_band(name='Hot Club of Gypsy Jazz', country='USA', isactive=True)
	# 	leband2 =  create_band(name='A fun band', country='USA', isactive=False)
	# 	lefestival1 = create_festival(name='Samois', country='France', isactive=True)
	# 	lefestival2 = create_festival(name='IGGF', country='UK', isactive=False)
	# 	lealbum = create_album(name='le first album', country='Norway')
	# 	lealbum = create_album(name='le second album', country='Italy')
	# 	levenue = create_venue(name='a fun venue', country='Norway', isactive=True)
	# 	levenue = create_venue(name='another fun venue', country='Italy', isactive=False)

	# 	request = ARequest(venue_country='France', venue='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(model_dict['venue']['qs'], [])
	# 	self.assertEqual(list(model_dict.keys()), ['venue'])

	# 	request = ARequest(venue='on')
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['venue']['qs']), ["<Venue: a fun venue>", "<Venue: another fun venue>"])
	# 	self.assertEqual(list(model_dict.keys()), ['venue'])

	# 	request = ARequest(venue='on', venue_country="Italy")
	# 	model_dict = filter_nodes(request)
	# 	self.assertQuerysetEqual(list(model_dict['venue']['qs']), ["<Venue: another fun venue>"])
	# 	self.assertEqual(list(model_dict.keys()), ['venue'])



