from django.shortcuts import render, redirect, get_object_or_404
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
from .forms import FestivalForm
from country_list import countries_for_language
COUNTRY_LIST = [(k, v) for k, v in dict(countries_for_language('en')).items()]


# Djangoverse forms
def post_festival(request):
	if request.method == 'POST':
		form = FestivalForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			return redirect('DjangoVerse:festival-list')
	else:
		form = FestivalForm()
	return render(request, 'DjangoVerse/festivalform.html', {'form': form})

def edit_festival(request, pk):
	festival = get_object_or_404(Festival, pk=pk)
	if request.method == 'POST':
		form = FestivalForm(request.POST, request.FILES, instance=festival)
		if form.is_valid():
			festival = form.save(commit=False)
			festival.save()
			return redirect('DjangoVerse:festival-list')
	else:
		form = FestivalForm(instance=festival)
	return render(request, 'Djangoverse/festivalform.html', {'form': form})



class BandViewSet(viewsets.ModelViewSet):
	queryset = Band.objects.all()
	serializer_class = BandSerializer

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

class SearchPlayer(generics.ListAPIView):
	serializer_class = PlayerSerializer

	def get_queryset(self):
		queryset = Player.objects.all()
		name_query = self.request.query_params.get("name", None)
		if name_query is not None:
			queryset = queryset.filter(name__startswith=name_query)
		return queryset


	
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
			model_dict[country_q[:-8]]['qs'] = model_dict[country_q[:-8]]['qs'].filter(country=request.query_params[country_q])
	else:
		pass

	list_filter_query = [e for e in ['instrument', 'active', 'name'] if e in request.query_params.keys()]
	if 'name' in request.query_params.keys():
		for k, v in model_dict.items():
			v['qs'] = v['qs'].filter(name__startswith=request.query_params['name'])
	if 'instrument' in request.query_params.keys():
		model_dict['player']['qs'] = model_dict['player']['qs'].filter(Q(instrument__name=request.query_params['instrument']))
	if 'active' in request.query_params.keys():
		for k, v in model_dict.items():
			v['qs'] = v['qs'].filter(isactive=request.query_params['active'])
	return model_dict

class SearchView(APIView):
	"""
	Toggle nodes on and off
	"""

	def get(self, request, format=None):
		model_dict = filter_nodes(request)

		for k, v in model_dict.items():
			v['ser'] = v['SerClass'](v['qs'], many=True, context={'request': request})
		return_list = []

		for vals in model_dict.values():
			for elem in vals['ser'].data:
				return_list.append(elem)

		return Response(return_list)





class D3View(APIView):
	"""
	API endpoint for D3
	"""

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
		'bands': reverse('DjangoVerse:band-list', request=request, format=format),
		'festivals': reverse('DjangoVerse:festival-list', request=request, format=format),
		# 'venues': reverse('DjangoVerse:venue-list', request=request, format=format),
		# 'albums': reverse('DjangoVerse:album-list', request=request, format=format),
		'instruments': reverse('DjangoVerse:instrument-list', request=request, format=format),
		})




