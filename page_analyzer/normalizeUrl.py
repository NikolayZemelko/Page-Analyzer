from validators.url import url
from urllib.parse import urlparse


def parse_url(s):
    fragmented_url = urlparse(s)
    true_sectioned_url = f'{fragmented_url.scheme}' + \
                         '://' + \
                         f'{fragmented_url.netloc}'
    parsed_url = true_sectioned_url.lower()
    return parsed_url


def valid_url(s):
    return url(s)
