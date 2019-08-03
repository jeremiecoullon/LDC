from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from DjangoVerse import views

list_dict = {
	'get': 'list',
    'post': 'create'
	}
detail_dict = {
	'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
	}

band_list = views.BandViewSet.as_view(list_dict)
band_detail = views.BandViewSet.as_view(detail_dict)

player_list = views.PlayerViewSet.as_view(list_dict)
player_detail = views.PlayerViewSet.as_view(detail_dict)

instrument_list = views.InstrumentViewSet.as_view(list_dict)
instrument_detail = views.InstrumentViewSet.as_view(detail_dict)

# album_list = views.AlbumViewSet.as_view(list_dict)
# album_detail = views.AlbumViewSet.as_view(detail_dict)

festival_list = views.FestivalViewSet.as_view(list_dict)
festival_detail = views.FestivalViewSet.as_view(detail_dict)

# venue_list = views.VenueViewSet.as_view(list_dict)
# venue_detail = views.VenueViewSet.as_view(detail_dict)


# commented out 'albums' and 'venue' URLS for now. Can add them later if needed
urlpatterns = [
	path('bands/', band_list, name='band-list'),
	path('bands/<str:pk>', band_detail, name='band-detail'),
	path('players/', player_list, name='player-list'),
	path('players/<str:pk>', player_detail, name='player-detail'),
	path('instruments/', instrument_list, name='instrument-list'),
	path('instruments/<str:pk>', instrument_detail, name='instrument-detail'),
	# path('albums/', album_list, name='album-list'),
	# path('albums/<str:pk>', album_detail, name='album-detail'),
	path('festivals/', festival_list, name='festival-list'),
	path('festivals/<str:pk>', festival_detail, name='festival-detail'),
	# path('venue/', venue_list, name='venue-list'),
	# path('venue/<str:pk>', venue_detail, name='venue-detail'),
	path('countries/', views.GetCountriesView.as_view(), name='country-list'),
	path('all_instruments/', views.GetInstrumentsView.as_view(), name='instrument-list'),
	# Search
	path('search/', views.SearchView.as_view()),

	path('D3endpoint/', views.D3View.as_view(), name='D3-endpoint'),
	path('', views.api_root)
]

urlpatterns = format_suffix_patterns(urlpatterns)