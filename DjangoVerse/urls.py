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

player_list = views.PlayerViewSet.as_view(list_dict)
player_detail = views.PlayerViewSet.as_view(detail_dict)

instrument_list = views.InstrumentViewSet.as_view(list_dict)
instrument_detail = views.InstrumentViewSet.as_view(detail_dict)

app_name = 'DjangoVerse'

# commented out 'albums' and 'venue' URLS for now. Can add them later if needed
urlpatterns = [
	path('players/', player_list, name='player-list'),
	path('players/<str:pk>', player_detail, name='player-detail'),
	path('instruments/', instrument_list, name='instrument-list'),
	path('instruments/<str:pk>', instrument_detail, name='instrument-detail'),
	path('countries/', views.GetCountriesView.as_view(), name='country-list'),
	path('all_instruments/', views.GetInstrumentsView.as_view(), name='instrument-list'),

	path('D3endpoint/', views.D3View.as_view(), name='D3-endpoint'),
	path('', views.api_root),

	# forms
	path("forms/player/add", views.post_player, name='add-player'),
	path("forms/player/<str:pk>/edit", views.edit_player, name='edit-player'),
	path("forms/player/list", views.form_list_player, name='list-player'),
	path("forms/player/<str:pk>/delete", views.delete_player, name='delete-player'),

	# forms
	path("forms/instrument/add", views.post_instrument, name='add-instrument'),
	path("forms/instrument/<str:pk>/edit", views.edit_instrument, name='edit-instrument'),
	path("forms/instrument/list", views.list_instruments, name='list-instruments'),
	
]

urlpatterns = format_suffix_patterns(urlpatterns)