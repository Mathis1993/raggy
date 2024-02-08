from urllib.parse import urlparse, urlunparse

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_and_normalize_url(requested_url):
    # Check if the URL has a scheme, if not, prepend "http://" by default
    parsed_url = urlparse(requested_url)
    if not parsed_url.scheme:
        # Default to "http" if no scheme is provided (consider "https" if secure by default)
        parsed_url = parsed_url._replace(scheme="http")

    normalized_url = urlunparse(parsed_url)
    validator = URLValidator()
    try:
        validator(normalized_url)
        return normalized_url
    except ValidationError:
        raise ValueError("Invalid URL provided.")
