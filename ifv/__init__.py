#!/usr/bin/env python
# encoding: utf-8

import copy
import logging

logger = logging.getLogger(__name__)


def not_implemented_function(*arguements):
    def wrapper(*args, **kwargs):
        raise NotImplementedError()
    return wrapper


class BaseAPIItem(object):

    def __init__(self, name):
        self._name = name

    def _cached_property(self, name, value):
        setattr(self, name, value)

    def _get_subitem(self, cls, name, *args, **kwargs):
        subitem = cls(name, *args, **kwargs)
        self._cached_property(name, subitem)
        return subitem


class BaseAPI(BaseAPIItem):
    BASE_CONTEXT = {}
    API_NAME = ""

    def __init__(self, *args, **kwargs):
        super(BaseAPI, self).__init__(self.API_NAME)
        self._context = copy.deepcopy(self.BASE_CONTEXT)

    def __getattr__(self, name):
        return self._get_subitem(APIPath, name, self)

    __call__ = not_implemented_function("api_path", "*args", "**kwargs")


class APIPath(BaseAPIItem):

    def __init__(self, name, root, parent=None):
        super(APIPath, self).__init__(name)
        self._parent = parent
        self._root = root
        self.__path = None

    @property
    def _path(self):
        if self.__path is None:
            if self._parent:
                self.__path = self._parent._path + (self._name,)
            else:
                self.__path = (self._name,)
        return self.__path

    def __getattr__(self, name):
        return self._get_subitem(
            self.__class__, name,
            self._root, self,
        )

    def __call__(self, *args, **kwargs):
        return self._root(self, *args, **kwargs)


class HTTPAPI(BaseAPI):

    def __init__(self, url):
        super(HTTPAPI, self).__init__()
        self._url = url

    _get_url = not_implemented_function("api_path")
    _get_method = not_implemented_function("api_path")
    _get_request = not_implemented_function(
        "url", "mehtod", "*args", "**kwargs"
    )
    _get_request_result = not_implemented_function("request")

    def __call__(self, api_path, *args, **kwargs):
        url = self._get_url(self, api_path._path)
        method = self._get_method(self, api_path)
        request = self._get_request(url, method, *args, **kwargs)
        return self._get_request_result(request)
