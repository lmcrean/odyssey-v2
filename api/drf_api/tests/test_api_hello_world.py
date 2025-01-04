"""
Module Docstring:
This module contains tests for the API endpoints.

python -m unittest drf_api/tests/test_api_hello_world.py

this is the command to run the tests
"""

import unittest
import requests
from ..lambda_function import lambda_handler

class HelloWorldAPITest(unittest.TestCase):
    """
    This class contains tests for the API endpoints.
    """
    def test_lambda_handler_returns_correct_response(self):
        """
        This method tests the lambda_handler function. It should return a 200 status code,
        a body of 'Hello World!', and the correct headers.
        """

        # Act
        response = lambda_handler()

        # Assert
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], 'Hello World!')
        self.assertEqual(
            response['headers']['Content-Type'],
            'application/json'
        )
        self.assertEqual(
            response['headers']['Access-Control-Allow-Origin'],
            '*'
        )

    def test_live_api_endpoint(self):
        """Test the actual deployed API endpoint"""
        # Arrange
        url = "https://b6kfw0mhn8.execute-api.eu-west-2.amazonaws.com/default/odyssey-hello-world"

        # Act
        response = requests.get(url, timeout=10.0)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello World!')
        self.assertEqual(
            response.headers['Content-Type'],
            'application/json'
        )
        self.assertEqual(
            response.headers['Access-Control-Allow-Origin'],
            '*'
        )

if __name__ == '__main__':
    unittest.main()
