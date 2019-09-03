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


def format_date(le_date):
    """
    Format date to display in gig list in the template.
    For example: "Sunday 27 January 2018"
    
    Parameters
    ----------
    le_date: Datetime.date

    Returns
    -------
    formatted_date: str
    """
    date_num = le_date.strftime("%d")
    if date_num[0]=='0':
        date_num=date_num[1]
    return le_date.strftime("%A ")+date_num + le_date.strftime(" %B %Y")