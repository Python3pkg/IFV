#!/usr/bin/env python
# encoding: utf-8

import unittest

import mock

import ifv


class TestBaseAPIItem(unittest.TestCase):

    def test_contruction(self):
        context = ifv.BaseAPIItem(name="test", value=1)
        self.assertEqual(context["name"], "test")
        self.assertEqual(context["value"], 1)

    def test_merged_context(self):
        parent_item = ifv.BaseAPIItem(name="parent", value=1)
        child_item = ifv.BaseAPIItem(parent_item, name="child")
        self.assertDictEqual(parent_item._merged_context, {
            "name": "parent", "value": 1,
        })
        self.assertDictEqual(child_item._merged_context, {
            "name": "child", "value": 1,
        })
        self.assertSetEqual(set(child_item), set(["name", "value"]))

    def test_parent_item(self):
        parent_item = ifv.BaseAPIItem(name="parent", value=1)
        child_item = ifv.BaseAPIItem(parent_item, name="child")
        self.assertEqual(parent_item["name"], "parent")
        self.assertEqual(parent_item["value"], 1)
        self.assertEqual(child_item["name"], "child")
        self.assertEqual(child_item["value"], 1)
        self.assertEqual(len(child_item), 2)

        with self.assertRaises(KeyError):
            parent_item["nothing"]

        with self.assertRaises(KeyError):
            child_item["nothing"]

        child_item["value"] = 2
        self.assertEqual(child_item["value"], 2)
        self.assertEqual(parent_item["value"], 1)

    def test_copy(self):
        parent_item = ifv.BaseAPIItem(name="parent", value=1)
        child_item1 = ifv.BaseAPIItem(parent_item, name="child", items=[])
        child_item2 = child_item1._copy()
        self.assertIs(child_item1._parent_item, child_item2._parent_item)
        self.assertIs(child_item1["items"], child_item2["items"])
        self.assertEqual(child_item1["name"], child_item2["name"])

    def test_subitem(self):
        parent_item = ifv.BaseAPIItem(name="parent", value=1)
        child_item = parent_item.child_item
        self.assertIs(parent_item, child_item._parent_item)
        self.assertDictEqual(
            parent_item._merged_context, child_item._merged_context,
        )

        with mock.patch(
            "ifv.BaseAPIItem._get_subitem_context",
            side_effect=lambda name: {"name": name},
        ):
            child_item2 = parent_item.child_item2
            self.assertIs(parent_item, child_item2._parent_item)
            self.assertEqual(child_item2["name"], "child_item2")

    @mock.patch(
        "ifv.BaseAPIItem.IGNORE_ERROR_TYPE",
        new_callable=mock.PropertyMock,
        return_value=[IndexError],
    )
    @mock.patch(
        "ifv.BaseAPIItem._handle_request_error",
        return_value=None,
    )
    def test_call(self, handle_request_error, IGNORE_ERROR_TYPE):
        parent_item = ifv.BaseAPIItem()
        with mock.patch(
            "ifv.BaseAPIItem._get_response_result",
            side_effect=lambda **kwargs: kwargs,
        ):
            result = parent_item.item.get(value=1)
            self.assertEqual(result, {"value": 1})

        with mock.patch(
            "ifv.BaseAPIItem._get_response_result",
            side_effect=ValueError,
        ):
            with self.assertRaises(ValueError):
                parent_item.item.get(value=1)

        with mock.patch(
            "ifv.BaseAPIItem._get_response_result",
            side_effect=IndexError,
        ):
            result = parent_item.item.get(value=1)
            self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
