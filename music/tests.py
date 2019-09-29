from django.test import TestCase
from .util import create_youtube_embed

class TestYoutubeParse(TestCase):

	def test_create_youtube_embed(self):
		"""
		Test the youtube URL processing function. It should either return an 'embed' style
		youtube or return an empty string.
		Try out a bunch of potential inputs in `url_dict`; keys are inputs and values are the expected outputs
		"""
		url_dict = {
		"https://www.youtube.com/embed/JWcaePIBLCU": "https://www.youtube.com/embed/JWcaePIBLCU?autoplay=1",
		"https://www.youtube.com/watch?v=cyZFhJbedA4": "https://www.youtube.com/embed/cyZFhJbedA4?autoplay=1",
		"https://www.youtube.com/embed/JWcaePIBLCU?autoplay=0": "https://www.youtube.com/embed/JWcaePIBLCU?autoplay=1",
		"": "",
		"Not a url!": "",
		"https://www.youtube.com/watch?v=mjnAE5go9dI&t=3337s": "https://www.youtube.com/embed/mjnAE5go9dI?autoplay=1",
		"https://www.youtube.com/watch?v=b_YHE4Sx-08": "https://www.youtube.com/embed/b_YHE4Sx-08?autoplay=1",
		"http://knowitwall.com/": "",
		"https://youtu.be/e8Dc2GJNOXo": "https://www.youtube.com/embed/e8Dc2GJNOXo?autoplay=1",
		"https://m.youtube.com/watch?v=sTibsyK7psk&feature=youtu.be": "https://www.youtube.com/embed/sTibsyK7psk?autoplay=1",
		}
		# create_episode(title="a fun Title with _underscores!", author_name="hip-ass author")
		# le_episode = Episode.objects.get(title="a fun Title with _underscores!")
		for raw_url, expected_url in url_dict.items():
			self.assertEqual(expected_url, create_youtube_embed(url=raw_url))
