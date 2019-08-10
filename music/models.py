from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from .util import create_youtube_embed, player_image_directory_path, tune_image_directory_path


def player_img_path(instance, filename):
	return f'LDC_Music/player_image/{instance.name}/{filename}'

class Tune(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(upload_to=tune_image_directory_path, null=True, blank=True)
	video_embed = models.CharField(default='', max_length=300, blank=True, verbose_name="Youtube URL")
	
	def save(self, *args, **kwargs):
		self.video_embed = create_youtube_embed(url=self.video_embed)
		super(Episode, self).save(*args, **kwargs)



class Player(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(upload_to=player_image_directory_path, null=True, blank=True)
	bio = RichTextField(default="player bio", config_name='default')
	image = models.ImageField(upload_to=player_img_path, null=True, blank=True)




class Volume(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(unique=True, max_length=200)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)

