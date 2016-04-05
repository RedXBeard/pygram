from urllib.error import URLError
from urllib.request import urlopen

__version__ = "1.0.0"
VERSION = __version__.split('.')


def printed(obj):
    if hasattr(obj, 'first_name'):
        return "{} {}".format(obj.first_name, obj.last_name)
    elif hasattr(obj, 'title'):
        return obj.title
    return ''


def check_version():
    try:
        resp = urlopen("https://github.com/RedXBeard/pygram/releases/latest")
        current_version = int("".join(resp.url.split("/")[-1].split(".")))
        if current_version > VERSION:
            return False
    except (URLError, ValueError):
        pass
    return True
