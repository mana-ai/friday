import re
import validators


def is_url(txt):
    return validators.url(txt)


def is_image_url(txt):
    if validators.url(txt):
        txt = str(txt).lower()
        if txt.endswith('.jpg') or txt.endswith('.png') or txt.endswith('.jpeg'):
            return True
        else:
            return False
    else:
        return False