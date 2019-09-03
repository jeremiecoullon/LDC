from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Player, Volume, Gig

def index(request):
	players = Player.objects.order_by('name')
	volumes = Volume.objects.order_by('name')
	return render(request, 'music/index.html', {'players': players, 'volumes': volumes})


def volume(request, slug):
	le_volume = get_object_or_404(Volume, slug=slug)
	if le_volume.status == "p" or request.user.is_staff:
		return render(request, 'music/volume_page.html', {'volume': le_volume})
	else:
		raise Http404()

def contact_gigs(request):
	gigs = Gig.objects.all()
	gigs = sorted(gigs, key=lambda x: x.gig_date_filter())
	return render(request, 'music/contact_gigs.html', {'gigs': gigs})

def DV(request):
	return render(request, 'DV/djangoverse_page.html')


def DV_fullscreen(request):
	return render(request, 'DV/DV_fullscreen.html')

def memes(request):
	return render(request, 'music/memes.html')
