import logging
import os

import config

from urllib.parse import unquote

logger = logging.getLogger('main')


# ToDo make URI validation func
class HttpRequest:
    def __init__(self, raw_request: str):
        self.raw_request = raw_request

        self.OK = False
        self.METHOD = None
        self.URI = None
        self.HTTP_VERSION = None

        self.PATH = None

        self.HEADERS = {}

        try:
            self._parse_headers()
            self._parse_uri()
        except Exception as e:
            logger.error(f"Error while request parsing: {str(e)}")
            return

    def _parse_headers(self):
        headers_list = self.raw_request.split("\r\n")

        if len(headers_list) == 0:
            logger.info("length is zero")
            return

        self.METHOD, self.URI, self.HTTP_VERSION = headers_list[0].split()

        self.METHOD = self.METHOD.upper()

        if self.HTTP_VERSION not in config.HTTP_ACCEPTABLE:
            logger.error(f"Error unacceptable http version: {self.HTTP_VERSION}")
            return

        for header in headers_list[1:]:
            header_name_value = header.split(": ")
            if len(header_name_value) != 2:
                logger.info("header has to many values")
                continue

            header_name, header_value = header.split(": ")

            self.HEADERS[header_name] = header_value

        self.OK = True

    def _parse_uri(self):
        if self.URI is not None:
            self.URI = unquote(self.URI.split("?")[0])
            self.PATH = config.PROJECT_ROOT.joinpath(os.path.realpath(self.URI[1:]))

    def __str__(self):
        return self.raw_request
