import uuid
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from country_list import countries_for_language

COUNTRY_LIST = [(k, v) for k, v in dict(countries_for_language('en')).items()]



def festival_img_path(instance, filename):
	return f'DjangoVerse/festival_images/{instance.name}/{filename}'

def venue_img_path(instance, filename):
	return f'DjangoVerse/venue_images/{instance.name}/{filename}'

def band_img_path(instance, filename):
	return f'DjangoVerse/band_images/{instance.name}/{filename}'

def player_img_path(instance, filename):
	return f'DjangoVerse/player_images/{instance.name}/{filename}'

def album_img_path(instance, filename): 
	return f'DjangoVerse/album_images/{instance.name}/{filename}'


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

def compress(image):
	im = Image.open(image)
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
	thumbnail = models.ImageField(upload_to=festival_img_path, null=True, blank=True)
	isactive = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.thumbnail = new_image
		# save
		super(Festival, self).save(*args, **kwargs)

class Venue(BaseInfo):
	image = models.ImageField(upload_to=venue_img_path, null=True, blank=True)
	thumbnail = models.ImageField(upload_to=venue_img_path, null=True, blank=True)
	isactive = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.thumbnail = new_image
		# save
		super(Venue, self).save(*args, **kwargs)

class Album(BaseInfo):
	image = models.ImageField(upload_to=album_img_path, null=True, blank=True)
	thumbnail = models.ImageField(upload_to=album_img_path, null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.thumbnail = new_image
		# save
		super(Venue, self).save(*args, **kwargs)

class Band(BaseInfo):
	image = models.ImageField(upload_to=band_img_path, null=True, blank=True)
	thumbnail = models.ImageField(upload_to=band_img_path, null=True, blank=True)
	isactive = models.BooleanField(default=True)
	festival = models.ManyToManyField(Festival, blank=True, related_name='bandsplayed')
	venue = models.ManyToManyField(Venue, blank=True, related_name='bandsplayed')
	album = models.ManyToManyField(Album, blank=True, related_name='band')

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.thumbnail = new_image
		# save
		super(Band, self).save(*args, **kwargs)



class Player(BaseInfo):
	instrument = models.ManyToManyField(Instrument)
	isactive = models.BooleanField(default=True)
	# not required
	image = models.ImageField(upload_to=player_img_path, null=True, blank=True)
	thumbnail = models.ImageField(upload_to=player_img_path, null=True, blank=True)
	band = models.ManyToManyField(Band, blank=True, related_name='members')
	festival = models.ManyToManyField(Festival, blank=True, related_name='playersplayed')
	venue = models.ManyToManyField(Venue, blank=True, related_name='playersplayed')
	album = models.ManyToManyField(Album, blank=True, related_name='playersplayed')

	def save(self, *args, **kwargs):
		if self.image:
			# call the compress function
			new_image = compress(self.image)
			# set self.image to new_image
			self.thumbnail = new_image
		# save
		super(Player, self).save(*args, **kwargs)
	


