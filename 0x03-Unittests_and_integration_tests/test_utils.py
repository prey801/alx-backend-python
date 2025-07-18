#!/usr/bin/env python3

"""Unit tests for the access_nested_map function."""

import unittest
from parameterized import parameterized
from typing import Any
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test class for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: Any) -> None:
        """
        Test that access_nested_map returns the expected result for valid inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, expected_key: str) -> None:
        """
        Test that access_nested_map raises KeyError with the expected message for invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")

