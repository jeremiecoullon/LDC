import os

def player_image_directory_path(instance, filename):
	# Author images will be uploaded to MEDIA_ROOT/Player_images/<author_name>/<filename>
	return 'Player_images/{0}/{1}'.format(instance.name, filename)

def tune_image_directory_path(instance, filename):
	# Author images will be uploaded to MEDIA_ROOT/Tune_images/<author_name>/<filename>
	return 'Tune_images/{0}/{1}'.format(instance.name, filename)


def create_youtube_embed(url):
    """
    Parses URL to youtube video and returns the embeded link.
    """
    if 'www.youtube.com' not in url:
        return ""
    if 'youtube.com/embed' in url:
        if "?" in url:
            url = url.split("?")[0]
        url = url.split('embed/')[-1]
        # return url
    if 'watch' in url:
        url = url.split("=")[1]
    if "&" in url:
        url = url.split("&")[0]
    return os.path.join('https://www.youtube.com','embed',url+'?autoplay=1')