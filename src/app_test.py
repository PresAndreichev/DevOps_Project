"""
This module contains tests for the Flask app.
"""

import unittest
from app import app

class TestApp(unittest.TestCase):
    """
    Test case for the Flask app's main routes and behavior.
    """

    def setUp(self):
        self.client = app.test_client()

    def test_hello_world(self):
        """
        Test that the '/hello' route returns the expected status code.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()