import logging
import re
from urllib.parse import urlparse

import tldextract

URL_MAX_LENGTH = 1024


class UrlStr(str):
    parsed_uri = None

    def __new__(cls, content):
        if isinstance(content, UrlStr):
            content, parsed_uri = str(content), content.parsed_uri
        else:
            content, parsed_uri = cls._sanitize_and_parse(str(content))

        if len(content) > URL_MAX_LENGTH:
            logging.warning("UrlStr with more than 1024 chars detected!")

        obj = super().__new__(cls, content[:URL_MAX_LENGTH])
        obj.parsed_uri = parsed_uri
        obj.top_level_domain = cls.get_top_level_domain(content)
        obj._domain_parts = None
        return obj

    @staticmethod
    def _sanitize_and_parse(url):
        if "://" not in url:
            url = f"://{url}"
        if url[0:3] == "://":
            url = f"http{url}"
        url = url.strip()
        parsed_uri = urlparse(url)

        domain = parsed_uri.netloc.strip()
        path = parsed_uri.path.strip()
        if not len(path):
            path = "/"
        path = re.sub(r"(/[/]+)", "/", path, flags=re.UNICODE + re.DOTALL)
        if path[0] != "/":
            path = f"/{path}"

        query = f"?{parsed_uri.query}" if parsed_uri.query else ""
        params = f";{parsed_uri.params}" if parsed_uri.params else ""
        fragment = f"#{parsed_uri.fragment}" if parsed_uri.fragment else ""
        url = f"{parsed_uri.scheme}://{domain}{path}{params}{query}{fragment}"

        return url, urlparse(url)

    @property
    def domain_parts(self):
        if self._domain_parts is None:
            self._domain_parts = self.parsed_uri.netloc.strip().split(".")
        return self._domain_parts

    def get_domain_parts(self) -> list:
        return self.domain_parts

    def get_domain(self, limit_to_domain_level: int = 5) -> str:
        domain = ".".join(self.parsed_uri.netloc.strip().split(".")[-1 * limit_to_domain_level :])
        if len(domain) > 255:
            raise ValueError(
                "parsed domain is longer than 255 chars, this shouldn't happen "
                "with normal domains!"
            )
        return domain

    @staticmethod
    def get_top_level_domain(url: str) -> str:
        return tldextract.extract(url).registered_domain
