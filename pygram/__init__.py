__version__ = "1.0.0"
VERSION = __version__.split('.')


def printed(obj):
    if hasattr(obj, 'first_name'):
        return "{} {}".format(obj.first_name, obj.last_name)
    elif hasattr(obj, 'title'):
        return obj.title
    return ''
