from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from .util import create_youtube_embed, player_image_directory_path, tune_image_directory_path


def player_img_path(instance, filename):
	return f'LDC_Music/player_image/{instance.name}/{filename}'

def volume_img_path(instance, filename):
	return f'LDC_Music/volume_image/{instance.name}/{filename}'

class Tune(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(upload_to=tune_image_directory_path, null=True, blank=True)
	video_embed = models.CharField(default='', max_length=300, blank=True, verbose_name="Youtube URL")
	band = RichTextField(default="list of musicians", config_name='default')
	
	def save(self, *args, **kwargs):
		self.video_embed = create_youtube_embed(url=self.video_embed)
		super(Tune, self).save(*args, **kwargs)

	def __str__(self):
		return self.name



class Player(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(upload_to=player_image_directory_path, null=True, blank=True)
	bio = RichTextField(default="player bio", config_name='default')
	image = models.ImageField(upload_to=player_img_path, null=True, blank=True)

	def __str__(self):
		return self.name




class Volume(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(unique=True, blank=True, max_length=200)
	image = models.ImageField(upload_to=volume_img_path, null=True, blank=True)
	composer = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE, related_name="composer")
	video_tune = models.ForeignKey(Tune, null=True, blank=True, on_delete=models.CASCADE, related_name="video_tune")
	audio_tune = models.ForeignKey(Tune, null=True, blank=True, on_delete=models.CASCADE, related_name="audio_tune")

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Volume, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

