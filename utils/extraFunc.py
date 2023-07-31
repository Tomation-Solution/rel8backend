from urllib import parse

from decimal import Decimal
import random
import string
from django.utils.encoding import force_str


def replace_query_param(url, key, val):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[force_str(key)] = [force_str(val)]
    query = parse.urlencode(sorted(query_dict.items()), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def generate_n(number:int=10):
    "helps u generate random char that are unqiue"
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(number))
