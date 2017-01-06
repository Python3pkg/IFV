#!/usr/bin/env python
# encoding: utf-8

import logging

logger = logging.getLogger(__name__)


class APIItemError(Exception):
    pass


class BaseAPIItem(object):
    BASE_CONTEXT = {}
    IGNORE_ERROR_TYPE = set([KeyboardInterrupt])

    @classmethod
    def _new(cls, parent_item=None, *args, **context):
        return cls(parent_item, *args, **context)

    def __init__(self, parent_item=None, *args, **kwargs):
        self._parent_item = parent_item
        self._context = kwargs

        if not parent_item:
            self._init_root(*args)

    def _init_root(self, *args):
        context = self.BASE_CONTEXT.copy()
        context.update(self._context)
        self._context = context

    def _copy(self):
        return self._new(self._parent_item, **self._context)

    def _is_ignore_request_error(self, error):
        error_type = type(error) if isinstance(error, Exception) else error
        if error_type in self.IGNORE_ERROR_TYPE:
            return True
        return False

    def _handle_request_error(self, error):
        logger.info(error)

    def _get_response_result(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_subitem_context(self, name):
        return None

    @property
    def _merged_context(self):
        context = {}
        if self._parent_item:
            context.update(self._parent_item._merged_context)
        context.update(self._context)
        return context

    def _get_subitem(self, name):
        context = self._get_subitem_context(name) or {}
        context.setdefault("item_name", name)
        return self._new(self, **context)

    def _get_item_list(self, key, strict=False):
        items = []
        item = self
        while item:
            if key in item._context:
                items.insert(0, item._context[key])
            elif not strict:
                items.insert(0, None)
            item = item._parent_item
        return items

    def __getattr__(self, name):
        return self._get_subitem(name)

    def __getitem__(self, key):
        try:
            return self._context[key]
        except (IndexError, KeyError):
            if self._parent_item:
                return self._parent_item[key]
            raise

    def __setitem__(self, key, value):
        self._context[key] = value

    def __iter__(self):
        return iter(self._merged_context)

    def __len__(self):
        return len(self._merged_context)

    def __call__(self, *args, **kwargs):
        try:
            return self._get_response_result(*args, **kwargs)
        except Exception as error:
            if self._is_ignore_request_error(error):
                return self._handle_request_error(error)
            else:
                raise
