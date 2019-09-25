from django.core.files import File
from io import BytesIO
from PIL import Image

def resize_image(image):
	"""
	Resize image to get a width/height ratio to be 1.5

	Parameters
	----------
	image: object from Image.open()
	"""
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
	"""
	Compress image

	Parameters
	----------
	image: object from Django's ImageField
	"""
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
