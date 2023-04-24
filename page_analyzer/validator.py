from validators.url import url
from urllib.parse import urlparse


def valid_url(s):
    return url(s)

