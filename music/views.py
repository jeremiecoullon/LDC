from django.shortcuts import render, get_object_or_404
from .models import Player, Volume

def index(request):
	players = Player.objects.order_by('name')
	volumes = Volume.objects.all()
	return render(request, 'music/index.html', {'players': players, 'volumes': volumes})


def volume(request, slug):
	le_volume = get_object_or_404(Volume, slug=slug)
	return render(request, 'music/volume_page.html', {'volume': le_volume})


def DV(request):
	return render(request, 'DV/djangoverse_page.html')
