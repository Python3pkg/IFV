#!/usr/bin/env python
# encoding: utf-8

import unittest

from ifv import http_api


class TestBaseHTTPAPI(unittest.TestCase):

    def test_usage(self):
        api = http_api.BaseHTTPAPI("http://your.dom.in/api")
        with self.assertRaises(NotImplementedError):
            api.services.monitor.create(host="127.0.0.1")
