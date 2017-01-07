# coding: utf-8

import logging

import requests

from ifv import BaseAPI, not_implemented_function

logger = logging.getLogger(__name__)


class BaseHTTPAPI(BaseAPI):

    def __init__(self, url):
        super(BaseHTTPAPI, self).__init__()
        self._url = url

    _get_request = not_implemented_function(
        "url", "mehtod", "*args", "**kwargs"
    )
    _get_request_result = not_implemented_function("request")
    _get_url = not_implemented_function("api_path")
    _get_method = not_implemented_function("api_path")

    def __call__(self, api_path, *args, **kwargs):
        url = self._get_url(api_path)
        method = self._get_method(api_path)
        request = self._get_request(url, method, *args, **kwargs)
        return self._get_request_result(request)
