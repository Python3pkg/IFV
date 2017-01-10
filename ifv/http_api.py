# coding: utf-8

import logging

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests

from ifv import BaseAPI, not_implemented_function

logger = logging.getLogger(__name__)


class NotAllowMethod(Exception):
    pass


class BaseHTTPAPI(BaseAPI):

    def __init__(self, url, headers=None):
        super(BaseHTTPAPI, self).__init__()
        self._url = url
        self._headers = headers or {}

    _get_request = not_implemented_function(
        "url", "mehtod", "*args", "**kwargs"
    )
    _get_request_result = not_implemented_function("request")
    _get_url_and_method = not_implemented_function("api_path")

    def __call__(self, api_path=None, *args, **kwargs):
        url, method = self._get_url_and_method(api_path)
        request = self._get_request(url, method, *args, **kwargs)
        return self._get_request_result(request)


class SimpleHTTPAPI(BaseHTTPAPI):
    DEFAULT_METHOD = "GET"
    METHOD_MAP = {
        "get": "GET",
        "post": "POST",
        "put": "PUT",
        "delete": "DELETE",
        "patch": "PATCH",
    }

    def __init__(self, *args, **kwargs):
        super(SimpleHTTPAPI, self).__init__(*args, **kwargs)
        self._session = requests.Session()

    _get_result_from_response = not_implemented_function("response")

    def _on_request_error(self, request, error):
        result = None
        handled = False
        return result, handled

    def _get_request(self, url, method, headers=(), **kwargs):
        kwargs["url"] = url
        kwargs["method"] = method
        request_headers = self._headers.copy()
        request_headers.update(headers)
        kwargs["headers"] = request_headers
        return kwargs

    def _get_url_and_method(self, api_path=None):
        if not api_path:
            return self._url, self.DEFAULT_METHOD

        url_paths = api_path._path[:-1]
        method_paths = api_path._path[-1:]
        url = urljoin(self._url, "/".join(url_paths))

        method_name = method_paths[0]
        method = self.METHOD_MAP.get(method_paths[0])
        if method is None:
            raise NotAllowMethod(method_name)
        return url, method

    def _get_request_result(self, request):
        try:
            response = self._session.request(**request)
        except Exception as error:
            result, handled = self._on_request_error(request, error)
            if not handled:
                raise
            return result
        return self._get_result_from_response(response)
