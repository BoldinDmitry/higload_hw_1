import os
from abc import ABC, abstractmethod
import logging

import config
from solution.http_tools.request.request import HttpRequest
from solution.http_tools.response.response import BaseHttpResponse, HttpResponseMethodNotAllowed, \
    HttpResponseBadResponse, HttpResponseForbidden, HttpResponseOK, HttpResponseNotFound


class BaseHandler(ABC):
    def _send_response(self, sock, response: BaseHttpResponse):
        logging.info(f"Sending response:{str(response)}")
        sock.sendall(response.encode())
        logging.info("Done")

    @abstractmethod
    def handle(self, sock):
        pass


class StaticHandler(BaseHandler):
    def handle(self, sock):

        logging.info('Start to process request')
        in_buffer = b''
        while not in_buffer.endswith(b'\n'):
            in_buffer += sock.recv(1024)
        logging.info('In buffer = ' + repr(in_buffer))

        raw_request = in_buffer.decode()
        request_http = HttpRequest(raw_request)

        if request_http.METHOD not in config.METHODS_ACCEPTABLE:
            self._send_response(sock, HttpResponseMethodNotAllowed())
            return

        if not request_http.OK:
            logging.info('Done with error')
            self._send_response(sock, HttpResponseBadResponse())
            return

        if config.MEDIA_ROOT not in request_http.PATH.parents:
            self._send_response(sock, HttpResponseForbidden())

        logging.info("PARSED OK")

        if os.path.isdir(request_http.PATH):
            request_http.PATH = str(request_http.PATH) + "/index.html"
            if not os.path.isfile(request_http.PATH):
                self._send_response(sock, HttpResponseForbidden())

        try:
            content = self._read_file(request_http.PATH)
        except Exception as e:
            logging.error(str(e))
            self._send_response(sock, HttpResponseNotFound())
            return

        response = HttpResponseOK(content, filename=request_http.PATH, with_body=request_http.METHOD != "HEAD")

        self._send_response(sock, response)

    def _read_file(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            content = f.read()
        return content
