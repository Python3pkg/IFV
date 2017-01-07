#!/usr/bin/env python
# encoding: utf-8

import logging

logger = logging.getLogger(__name__)


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

    def __init__(self, *args, **kwargs):
        super(BaseAPI, self).__init__("")
        self._context = self.BASE_CONTEXT.copy()

    def __getattr__(self, name):
        return self._get_subitem(APIPath, name, self)

    def __call__(self, api_path, *args, **kwargs):
        raise NotImplementedError()


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
