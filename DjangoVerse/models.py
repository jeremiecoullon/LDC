import uuid
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from country_list import countries_for_language
from music.util import create_youtube_embed

COUNTRY_LIST = [(k, v) for k, v in dict(countries_for_language('en')).items()]


def player_img_path(instance, filename):
	"Always give the same name to a player image (based on name and id)"
	return f'DjangoVerse/player_images/{instance.name}_{instance.id}.jpg'

def festival_img_path(instance, filename):
	return f'DjangoVerse/festival_images/{instance.name}_{instance.id}.jpg'

def venue_img_path(instance, filename):
	return f'DjangoVerse/venue_images/{instance.name}_{instance.id}.jpg'

def band_img_path(instance, filename):
	return f'DjangoVerse/band_images/{instance.name}_{instance.id}.jpg'

def album_img_path(instance, filename): 
	return f'DjangoVerse/album_images/{instance.name}_{instance.id}.jpg'


class BaseInfo(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	country = models.CharField(choices=COUNTRY_LIST, max_length=200)
	# not required
	description = models.CharField(max_length=200, blank=True)
	external_URL = models.CharField(max_length=300, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True



class Instrument(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


def resize_image(image):
	width, height = image.size
	if abs(width/height - (1.5)) <= 0.1:
		pass
	elif (width/height) < 1.4:
		# crop_height: remove an equal amount from both sides
		left = 0
		right = width
		top = height/2 - (1/3)*width
		bottom = height/2 + (1/3)*width
		image = image.crop((left, top, right, bottom))
	elif (width/height) > 1.6:
		# crop width: remove an equal amount from both sides
		left = (width/2) - (3/4)*height
		right = (width/2) + (3/4)*height
		top = 0
		bottom = height
		image = image.crop((left, top, right, bottom))
	return image	
def compress(image):
	im = Image.open(image)
	# resize image if the ratio isn't approimately width/height = 1.5:
	im = resize_image(image=im)

	# create a BytesIO object
	im = im.convert('RGB')
	im_io = BytesIO() 
	# save image to BytesIO object
	im.save(im_io, 'JPEG', quality=70) 
	# create a django-friendly Files object
	new_image = File(im_io, name=image.name)
	return new_image

class Festival(BaseInfo):
	# image = models.ImageField(upload_to=festival_img_path, null=True, blank=True)
	image = models.ImageField(upload_to=festival_img_path, null=True, blank=True)
	isactive = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.image = new_image
		# save
		super(Festival, self).save(*args, **kwargs)

class Venue(BaseInfo):
	image = models.ImageField(upload_to=venue_img_path, null=True, blank=True)
	isactive = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.image = new_image
		# save
		super(Venue, self).save(*args, **kwargs)

class Album(BaseInfo):
	image = models.ImageField(upload_to=album_img_path, null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.image = new_image
		# save
		super(Album, self).save(*args, **kwargs)

class Band(BaseInfo):
	image = models.ImageField(upload_to=band_img_path, null=True, blank=True)
	isactive = models.BooleanField(default=True)
	festival = models.ManyToManyField(Festival, blank=True, related_name='bandsplayed')
	venue = models.ManyToManyField(Venue, blank=True, related_name='bandsplayed')
	album = models.ManyToManyField(Album, blank=True, related_name='band')

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.image = new_image
		# save
		super(Band, self).save(*args, **kwargs)


instrument_help_text = """
<p>This field is required!</p>
<hr>
<p><span style='font-weight:bold'>On desktop:</span> double click on an instrument to select it</p>
<p style='font-weight:bold'>On mobile:</p>
<ol>
<li>Click on the gray box in the 'available instrument' group, choose an instrument, and click OK.</li>
<li>Click on the downward arrow to move the instrument to the 'chosen instrument' group</li>
</ol>
"""

gigged_with_help_text = """
<p>Choose people this player has gigged with (ie: done a concert with). Note that jams don't count!</p>
<hr>
<p><span style='font-weight:bold'>On desktop:</span> double click on a player to select them</p>
<p style='font-weight:bold'>On mobile:</p>
<ol>
<li>Click on the gray box in the 'available gigged with' group, choose some players, and click OK.</li>
<li>Click on the downward arrow to move the players to the 'chosen gigged with' group</li>
</ol>
"""


class Player(BaseInfo):
	instrument = models.ManyToManyField(Instrument, help_text=instrument_help_text)
	isactive = models.BooleanField(default=True, help_text="Whether or not they're active on the Gypsy Jazz scene today")
	# not required
	image = models.ImageField(upload_to=player_img_path, null=True, blank=True, help_text="If the width is not 1.5 times the height, then the image will be cropped to make it so.")
	band = models.ManyToManyField(Band, blank=True, related_name='members')
	festival = models.ManyToManyField(Festival, blank=True, related_name='playersplayed')
	venue = models.ManyToManyField(Venue, blank=True, related_name='playersplayed')
	album = models.ManyToManyField(Album, blank=True, related_name='playersplayed')
	gigged_with = models.ManyToManyField('self', blank=True, help_text=gigged_with_help_text)
	video_embed = models.CharField(default='', max_length=300, blank=True, verbose_name="Youtube URL", help_text="Paste the URL to a youtube video of this player's music")

	def save(self, *args, **kwargs):
		self.video_embed = create_youtube_embed(url=self.video_embed)
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.image = new_image
		# save
		super(Player, self).save(*args, **kwargs)
	


