#!/usr/bin/env python
# encoding: utf-8

import logging

logger = logging.getLogger(__name__)


class BaseAPIItem(object):
    IGNORE_ERROR_TYPE = set([KeyboardInterrupt])

    def __init__(self, parent_item=None, **kwargs):
        self._context = kwargs
        self._parent_item = parent_item

    def _copy(self):
        return BaseAPIItem(self._parent_item, **self._context)

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

    def __getattr__(self, name):
        context = self._get_subitem_context(name) or {}
        return BaseAPIItem(self, **context)

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
