#!/usr/bin/env python3
'''Module for testing utility functions.'''
from parameterized import parameterized
import unittest
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    '''Test cases for access_nested_map function.'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Check if access_nested_map returns the expected result."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Check if KeyError is raised with the expected message."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(error.exception))


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, payload):
        """Check if get_json returns the expected payload."""
        mock_response = {'return_value.json.return_value': payload}
        with patch('requests.get', **mock_response) as mock_get:
            self.assertEqual(get_json(url), payload)
            mock_get.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Test cases for memoize function."""

    def test_memoize(self):
        """Check if a_property is computed only once using memoize."""

        class TestClass:
            """Class to test memoization."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mocked_method:
            test_obj = TestClass()
            test_obj.a_property()
            test_obj.a_property()
            mocked_method.assert_called_once()
