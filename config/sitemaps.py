from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from music.models import Volume
 
 
class VolumeSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.9

	def items(self):
		return Volume.objects.filter(status='p')


class IndexViewSitemap(Sitemap):
	changefreq = "never"
	priority = 1

	def items(self):
		return ['music:index']

	def location(self, item):
		return reverse(item)


class OtherStaticViewSitemap(Sitemap):
	changefreq = "never"
	priority = 0.8

	def items(self):
		return ['music:contact-gigs', 'music:memes-page', 'DjangoVerse:djangoverse-page']

	def location(self, item):
		return reverse(item)