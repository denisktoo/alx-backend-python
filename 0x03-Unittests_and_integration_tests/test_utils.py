#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
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
    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
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
