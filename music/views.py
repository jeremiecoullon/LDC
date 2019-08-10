from django.shortcuts import render
from .models import Player

def index(request):
	players = Player.objects.order_by('name')
	return render(request, 'music/index.html', {'players': players})
