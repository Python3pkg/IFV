#!/usr/bin/env python
# encoding: utf-8

import unittest

import mock

from ifv import http_api


class TestBaseHTTPAPI(unittest.TestCase):

    def test_usage(self):
        api = http_api.BaseHTTPAPI("http://your.dom.in/api")
        with self.assertRaises(NotImplementedError):
            api.services.monitor.create(host="127.0.0.1")


class TestSimpleHTTPAPI(unittest.TestCase):

    def setUp(self):
        self.api = http_api.SimpleHTTPAPI("http://your.dom.in/")

    def test_get_url_and_method(self):
        url, method = self.api._get_url_and_method()
        self.assertEqual(url, "http://your.dom.in/")
        self.assertEqual(method, "GET")

        url, method = self.api._get_url_and_method(self.api.get)
        self.assertEqual(url, "http://your.dom.in/")
        self.assertEqual(method, "GET")

        url, method = self.api._get_url_and_method(self.api.path.to.st.post)
        self.assertEqual(url, "http://your.dom.in/path/to/st")
        self.assertEqual(method, "POST")

        with self.assertRaises(http_api.NotAllowMethod):
            self.api._get_url_and_method(self.api.not_allow)

    @mock.patch(
        "ifv.http_api.SimpleHTTPAPI._get_result_from_response",
        side_effect=lambda r: r,
    )
    def test_get_request_result(self, _get_result_from_response):
        with mock.patch(
            "requests.Session.request", side_effect=lambda **k: k,
        ):
            result = self.api.path.to.st.post(value=1)
            self.assertDictContainsSubset({
                "url": "http://your.dom.in/path/to/st",
                "method": "POST",
                "value": 1,
            }, result)

        with mock.patch(
            "requests.Session.request", side_effect=NotImplementedError,
        ):
            with self.assertRaises(NotImplementedError):
                result = self.api.path.to.st.post(value=1)

            with mock.patch(
                "ifv.http_api.SimpleHTTPAPI._on_request_error",
                side_effect=lambda *a, **k: (id(self), True),
            ):
                result = self.api.path.to.st.post(value=1)
                self.assertEqual(result, id(self))

    @mock.patch(
        "ifv.http_api.SimpleHTTPAPI._get_result_from_response",
        side_effect=lambda r: r,
    )
    def test_set_headers(self, _get_result_from_response):
        with mock.patch(
            "requests.Session.request", side_effect=lambda **k: k,
        ):
            result = self.api.path.to.st.post(headers={
                "name": "test",
            })
            self.assertDictContainsSubset({
                "headers": {"name": "test"},
            }, result)

            self.api._headers["value"] = "hello"
            result = self.api.path.to.st.post()
            self.assertDictContainsSubset({
                "headers": {"value": "hello"},
            }, result)

            result = self.api.path.to.st.post(headers={
                "name": "test",
            })
            self.assertDictContainsSubset({
                "headers": {
                    "name": "test",
                    "value": "hello",
                },
            }, result)
