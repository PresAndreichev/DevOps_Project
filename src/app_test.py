import unittest

from app import app


class TestApp(unittest.TestCase):
    """Unit tests for the Flask app."""

    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()

    def test_hello_world(self):
        """Test that the root endpoint returns a 200 status code."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()