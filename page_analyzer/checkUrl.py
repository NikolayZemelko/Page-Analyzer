import validators
from urllib.parse import urlparse


def normalize_url(s):

    if s:
        fragmented_url = urlparse(s)
        true_sectioned_url = f'{fragmented_url.scheme}' + \
                             '://' + \
                             f'{fragmented_url.netloc}'
        normalized_url = true_sectioned_url.lower()
        return normalized_url


def valid_url(s):

    if s:
        if validators.url(s):
            fragmented_url = urlparse(s)
            has_scheme = fragmented_url.scheme

            return has_scheme
