#!/usr/bin/env python3
"""
Unittests for utils module.

This module contains unit tests for the following utility functions:
- access_nested_map
- get_json
- memoize
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected value
        for a valid path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises a KeyError
        for an invalid path.
        """
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test cases for the get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        """
        Test that get_json returns the expected JSON payload
        and that requests.get is called once with the correct URL.
        """
        # create a mock response and configure it
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_payload

        # make requests.get return the mock response
        mock_requests_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assertions
        mock_requests_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test cases for the memoize decorator.
    """

    def test_memoize(self):
        """
        Test that memoize caches the result of a method
        and that the underlying method is called only once.
        """
        class TestClass:
            """
            Test class with a_method and a memoized a_property.
            """

            def a_method(self):
                """Simple method returning 42."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_a_method:
            obj = TestClass()

            # Call a_property twice
            result_1 = obj.a_property
            result_2 = obj.a_property

            # Both results should be correct
            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)

            # a_method should only be called once
            mock_a_method.assert_called_once()
