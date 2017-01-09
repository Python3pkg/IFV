#!/usr/bin/env python
# encoding: utf-8

import unittest

import mock

import ifv


class TestNotImplementedFunction(unittest.TestCase):

    def test_call(self):
        func = ifv.not_implemented_function("arg1", "arg2")
        with self.assertRaises(NotImplementedError):
            func(1, 2)


class TestBaseAPIItem(unittest.TestCase):

    def test_construction(self):
        item = ifv.BaseAPIItem("test")
        self.assertEqual(item._name, "test")

    def test_cached_property(self):
        item = ifv.BaseAPIItem("test")
        value = []
        item._cached_property("value", value)
        self.assertIs(item.value, value)

    def test_get_subitem(self):
        item = ifv.BaseAPIItem("test")
        subitem = item._get_subitem(ifv.BaseAPIItem, "subitem")
        self.assertIs(subitem, item.subitem)


class TestBaseAPI(unittest.TestCase):

    def test_construction(self):
        item = ifv.BaseAPI()
        self.assertIs(item.subitem, item.subitem)
        self.assertEqual(item.subitem._name, "subitem")
        with self.assertRaises(AttributeError):
            item._subitem

        item2 = ifv.BaseAPI()
        self.assertIsNot(item._context, item2._context)


class TestAPIPath(unittest.TestCase):

    def setUp(self):
        self.root = mock.MagicMock()

    def test_construction(self):
        item = ifv.APIPath("test", self.root)
        self.assertIs(item._root, self.root)
        self.assertIsNone(item._parent)
        self.assertTupleEqual(item._path, ("test",))

    def test_subitem(self):
        item = ifv.APIPath("test", self.root)
        self.assertIs(item.subitem, item.subitem)
        with self.assertRaises(AttributeError):
            item._subitem

    def test_path(self):
        item = ifv.APIPath("test", self.root)
        self.assertTupleEqual(item.subitem._path, ("test", "subitem"))
