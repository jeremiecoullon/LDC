from django.shortcuts import render, get_object_or_404
from .models import Player, Volume

def index(request):
	players = Player.objects.order_by('name')
	volumes = Volume.objects.order_by('name')
	return render(request, 'music/index.html', {'players': players, 'volumes': volumes})


def volume(request, slug):
	le_volume = get_object_or_404(Volume, slug=slug)
	return render(request, 'music/volume_page.html', {'volume': le_volume})

def contact_gigs(request):
	return render(request, 'music/contact_gigs.html')

def DV(request):
	return render(request, 'DV/djangoverse_page.html')


def DV_fullscreen(request):
	return render(request, 'DV/DV_fullscreen.html')

