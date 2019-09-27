from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import filters

from django.db.models import Q
from DjangoVerse.serializers import BandSerializer, PlayerSerializer, LinkPlayerSerializer, InstrumentSerializer, VenueSerializer, FestivalSerializer, AlbumSerializer, LinkBandSerializer
from DjangoVerse.serializers import BandCountrySerializer, PlayerCountrySerializer, VenueCountrySerializer, FestivalCountrySerializer, AlbumCountrySerializer
from DjangoVerse.models import Band, Player, Instrument, Venue, Festival, Album
from music.models import Volume
from .forms import PlayerForm, InstrumentForm
from country_list import countries_for_language
import itertools
COUNTRY_LIST = [(k, v) for k, v in dict(countries_for_language('en')).items()]


# Djangoverse forms: players
def post_player(request):
	if request.method == 'POST':
		form = PlayerForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=True)
			# 3 'save' buttons in the form:
			if 'btn-save' in request.POST:
				return redirect("DjangoVerse:list-player")
			elif 'btn-save-and-continue' in request.POST:
				return redirect("DjangoVerse:edit-player", pk=post.pk)
			elif 'btn-save-and-DjangoVerse' in request.POST:
				return redirect("music:djangoverse-page")	
	else:
		form = PlayerForm()
	volumes = Volume.objects.order_by('name')
	return render(request, 'DjangoVerse/playerform.html', {'volumes': volumes, 'form': form})
	

def edit_player(request, pk):
	player = get_object_or_404(Player, pk=pk)
	if request.method == 'POST':
		form = PlayerForm(request.POST, request.FILES, instance=player)
		if form.is_valid():
			player = form.save(commit=True)
			
			# 3 'save' buttons in the form:
			if 'btn-save' in request.POST:
				return redirect("DjangoVerse:list-player")
			elif 'btn-save-and-continue' in request.POST:
				return redirect("DjangoVerse:edit-player", pk=pk)
			# elif 'btn-save-and-add' in request.POST:
			# 	return redirect("DjangoVerse:add-player")
			elif 'btn-save-and-DjangoVerse' in request.POST:
				return redirect("music:djangoverse-page")	
	else:
		form = PlayerForm(instance=player)
	return render(request, 'DjangoVerse/playerform.html', {'player': player, 'form': form})

def form_list_player(request):
	players = Player.objects.order_by('name')
	return render(request, 'DjangoVerse/playerlist.html', {'players': players})


def delete_player(request, pk):
	cache.clear()
	player = get_object_or_404(Player, pk=pk)
	if request.method == 'POST':
		player.delete()
		return redirect("DjangoVerse:list-player")
	return render(request, 'DjangoVerse/delete_page.html', {'player': player})


# =============

def post_instrument(request):
	if request.method == 'POST':
		form = InstrumentForm(request.POST)
		if form.is_valid():
			post = form.save(commit=True)
			return redirect("DjangoVerse:list-instruments")
	else:
		form = InstrumentForm()
	volumes = Volume.objects.order_by('name')
	return render(request, 'DjangoVerse/instrumentform.html', {'volumes': volumes, 'form': form})

def edit_instrument(request, pk):
	instrument = get_object_or_404(Instrument, pk=pk)
	if request.method == 'POST':
		form = InstrumentForm(request.POST, instance=instrument)
		if form.is_valid():
			instrument = form.save(commit=True)
			
			# 3 'save' buttons in the form:
			if 'btn-save' in request.POST:
				return redirect("DjangoVerse:list-instruments")
			elif 'btn-save-and-continue' in request.POST:
				return redirect("DjangoVerse:edit-instrument", pk=pk)
			elif 'btn-save-and-add' in request.POST:
				return redirect("DjangoVerse:add-instrument")
	else:
		form = InstrumentForm(instance=instrument)
	return render(request, 'DjangoVerse/instrumentform.html', {'instrument': instrument, 'form': form})

def list_instruments(request):
	instruments = Instrument.objects.order_by('name')
	return render(request, 'DjangoVerse/instrumentlist.html', {'instruments': instruments})

# class BandViewSet(viewsets.ModelViewSet):
# 	queryset = Band.objects.all()
# 	serializer_class = BandSerializer

class PlayerViewSet(viewsets.ModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

class InstrumentViewSet(viewsets.ModelViewSet):
	queryset = Instrument.objects.all()
	serializer_class = InstrumentSerializer

class FestivalViewSet(viewsets.ModelViewSet):
	queryset = Festival.objects.all()
	serializer_class = FestivalSerializer

# class VenueViewSet(viewsets.ModelViewSet):
# 	queryset = Venue.objects.all()
# 	serializer_class = VenueSerializer

# class AlbumViewSet(viewsets.ModelViewSet):
# 	queryset = Album.objects.all()
# 	serializer_class = AlbumSerializer



	
class GetCountriesView(APIView):
	"""
	Get all unique used countries for a given model.
	Returns both short version and human readable 
	Ex: {
		'band': [('GB', 'United Kingdom'), ('FR', 'France')],
		'festival': [('FR', 'France')],
			}
	"""

	def get(self, request, format=None):

		model_dict = {'band': {'qs': Band.objects.values('country').distinct(), 'SerClass': BandCountrySerializer}, 
				"player": {'qs': Player.objects.values('country').distinct(), 'SerClass': PlayerCountrySerializer},
				"venue": {'qs': Venue.objects.values('country').distinct(), 'SerClass': VenueCountrySerializer},
				"festival": {'qs': Festival.objects.values('country').distinct(), 'SerClass': FestivalCountrySerializer},
				"album": {'qs': Album.objects.values('country').distinct(), 'SerClass': AlbumCountrySerializer},
				}

		return_dict = {}
		for k, v in model_dict.items():
			return_dict.update({k: v['SerClass'](v['qs'], many=True, context={'request': request}).data})
		
		new_return_dict = {}
		for k,v in return_dict.items():
			# convert to a list of human readable countries
			new_return_dict[k] = [(elem["country"], dict(COUNTRY_LIST)[elem["country"]]) for elem in v]

		return Response(new_return_dict)

class GetInstrumentsView(APIView):
	"""
	Get all unique used countries for a given model.
	Returns both short version and human readable 
	Ex: {
		'band': [('GB', 'United Kingdom'), ('FR', 'France')],
		'festival': [('FR', 'France')],
			}
	"""

	def get(self, request, format=None):
		instruments = Instrument.objects.all()
		serialiser = InstrumentSerializer(instruments, many=True, context={'request': request})
		return_dict = {'instruments': serialiser.data}
		return Response({'instruments': [v['name'] for v in return_dict['instruments']]})


def filter_nodes(request):
	"""
	Filter the nodes based on a request and return a model_dict

	Example filters:

	'?player=on'
	'?festival=on'
	'?band_country=GB'
	'?active=True'
	'?instrument=Violin'
	"""
	model_dict = {'band': {'qs': Band.objects.all(), 'SerClass': BandSerializer}, 
				"player": {'qs': Player.objects.all(), 'SerClass': PlayerSerializer},
				"venue": {'qs': Venue.objects.all(), 'SerClass': VenueSerializer},
				"festival": {'qs': Festival.objects.all(), 'SerClass': FestivalSerializer},
				"album": {'qs': Album.objects.all(), 'SerClass': AlbumSerializer},
				}

	list_nodes_on = [elem for elem in ['player', 'band', 'venue', 'festival', 'album'] if elem in request.query_params.keys()]
	model_dict = {k:model_dict[k] for k in list_nodes_on}

	list_country_query = [e for e in ['player_country', 'band_country', 'venue_country', 'festival_country', 'album_country'] if e in request.query_params.keys()]
	# check that the nodes in the list_country_query are also selected !
	list_country_query = [e for e in list_country_query if e[:-8] in list_nodes_on]

	# filter each country
	if list_country_query != []:
		for country_q in list_country_query:
			
			# for player_countries: treat it as a list so you query several countries at once
			if (country_q == 'player_country') and (hasattr(request.query_params, "getlist")):
				query_list_countries = request.query_params.getlist('player_country')
				# have several countries in the filter
				Q_query_filter = Q()
				for ql in query_list_countries:
					Q_query_filter |= Q(country=ql)
				model_dict[country_q[:-8]]['qs'] = model_dict[country_q[:-8]]['qs'].filter(Q_query_filter)

			# for everything else: only filter one option at a time
			else:
				model_dict[country_q[:-8]]['qs'] = model_dict[country_q[:-8]]['qs'].filter(country=request.query_params[country_q])
	else:
		pass

	list_filter_query = [e for e in ['instrument', 'active', 'name'] if e in request.query_params.keys()]
	if 'name' in request.query_params.keys():
		for k, v in model_dict.items():
			v['qs'] = v['qs'].filter(name__startswith=request.query_params['name'])
	
	if 'instrument' in request.query_params.keys():
		# build the query filter so that you can query several instruments at once
		Q_query_filter = Q()
		for ql in request.query_params.getlist('instrument'):
			Q_query_filter |= Q(instrument__name=ql)
		model_dict['player']['qs'] = model_dict['player']['qs'].filter(Q_query_filter)

	if 'active' in request.query_params.keys():
		for k, v in model_dict.items():
			v['qs'] = v['qs'].filter(isactive=request.query_params['active'])
	return model_dict





class D3View(APIView):
	"""
	API endpoint for D3. 
	
	Query parameters:
	----------------
	'?player=on': queries players
	'player_country=FR': filters for players based in France
	'instrument=Guitar': filters for guitar players
	'active=True': filters for active players
	
	=====================

	Code is super bloated as at first it deals with a bunch of different models..
	Note: the first few lines create the list of nodes, and the bit between 'Start' and 'End' creates links between players.
	The rest of it deals with the other models (so doesn't get called if you don't inlude 'band', 'venue', or 'festival' in the query)
	"""
	@method_decorator(cache_page(60*60*2))
	def get(self, request, format=None):
		# filter based on the request
		model_dict = filter_nodes(request)
		# put together node data
		node_list = []
		for k,v in model_dict.items():
			# create serializer
			v['ser'] = v['SerClass'](v['qs'], many=True, context={'request': request})
			for elem in v['ser'].data:
				elem.update({'type': k})
				node_list.append(elem)



		# put together link data
		link_list = []

		# list_player_id = [e[0] for e in model_dict['player']['qs'].values_list('id')]
		# print(list_player_id)


		if 'player' in request.query_params.keys():
			linkplayerserializer = LinkPlayerSerializer(model_dict['player']['qs'], many=True, context={'request': request})
			other_model_list = [e for e in ['band', 'festival', 'venue', 'album'] if e in request.query_params.keys()]

			# ================================================
			# Start: Create links between players
			# ================================================
			# define a new list that will have a bunch of 2-lists in it (with duplicates)
			gigged_with_list = []
			for od in linkplayerserializer.data:
				for otherplayer in od['gigged_with']:
					gigged_with_list.append([od['id'], str(otherplayer)])

			# sort each 2-list in gigged_with_list
			for e in gigged_with_list:
				e.sort()

			# remove duplicate 2-lists (see https://stackoverflow.com/questions/2213923/removing-duplicates-from-a-list-of-lists)
			gigged_with_list.sort()
			no_dup_gigged_with_list = list(gigged_with_list for gigged_with_list,_ in itertools.groupby(gigged_with_list))

			# append list of unique 2-lists to link_list
			filtered_ids = [elem['id'] for elem in linkplayerserializer.data]
			for elem in no_dup_gigged_with_list:
				# if either source or target is not in the list of filtered IDs, then move on to the next pair of nodes
				if elem[0] not in filtered_ids or elem[1] not in filtered_ids:
					continue
				link_list.append({'source': elem[0], 'target': elem[1]})
			# ================================================
			# End of creating links between players
			# ================================================

			for elem in linkplayerserializer.data:
				for othermodel in other_model_list:
					# get list of UUID of 'other model' (ie: the model for the ManyToMany relationship).
					# Drop the related IDs that should have been filtered out
					list_othermodel_id = [e[0] for e in model_dict[othermodel]['qs'].values_list('id')]
					for eachelem in elem[othermodel]:
						if eachelem not in list_othermodel_id:
							continue
						link_list.append({'source': elem['id'], 'target': eachelem})
		else: pass
		if 'band' in request.query_params.keys():
			linkbandserializer = LinkBandSerializer(model_dict['band']['qs'], many=True, context={'request': request})
			other_model_list = [e for e in ['festival', 'venue', 'album'] if e in request.query_params.keys()]
			for elem in linkbandserializer.data:
				for othermodel in other_model_list:
					list_othermodel_id = [e[0] for e in model_dict[othermodel]['qs'].values_list('id')]
					for eachelem in elem[othermodel]:
						if eachelem not in list_othermodel_id:
							continue
						link_list.append({'source': elem['id'], 'target': eachelem})
		else: pass

		data_dict = {'nodes': node_list, 'links': link_list}
		return Response(data_dict)


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'D3_endpoint': reverse('DjangoVerse:D3-endpoint', request=request, format=format),
		'players': reverse('DjangoVerse:player-list', request=request, format=format),
		# 'bands': reverse('DjangoVerse:band-list', request=request, format=format),
		# 'festivals': reverse('DjangoVerse:festival-list', request=request, format=format),
		# 'venues': reverse('DjangoVerse:venue-list', request=request, format=format),
		# 'albums': reverse('DjangoVerse:album-list', request=request, format=format),
		'instruments': reverse('DjangoVerse:instrument-list', request=request, format=format),
		})




