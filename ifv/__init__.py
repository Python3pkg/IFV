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
        return self._get_subitem(
            APIPath, name, self,
        )


class APIPath(BaseAPIItem):

    def __init__(self, name, root, parent=None):
        super(APIPath, self).__init__(name)
        self._parent = parent
        self._root = root
        self.__path = None

    def __getattr__(self, name):
        return self._get_subitem(
            self.__class__, name, self._root, self,
        )

    @property
    def _path(self):
        if self.__path is None:
            if self._parent:
                self.__path = self._parent._path + (self._name,)
            else:
                self.__path = (self._name,)
        return self.__path

    def __call__(self, *args, **kwargs):
        return self._root(self, *args, **kwargs)
