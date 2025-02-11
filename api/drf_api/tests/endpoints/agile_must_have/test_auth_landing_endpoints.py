"""
Tests for authentication-related API endpoints.
Verifies endpoint health and response formats in both local and production environments.
"""

import unittest
import requests
import os
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthEndpointTests(unittest.TestCase):
    """Test suite for auth endpoints."""
    @classmethod
    def setUpClass(cls):
        """Set up base URLs and test data."""
        cls.local_url = 'http://localhost:8000'
        cls.prod_url = 'https://b6kfw0mhn8.execute-api.eu-west-2.amazonaws.com/default'
        cls.headers = {'Content-Type': 'application/json'}

    def setUp(self):
        """Set up test-specific data."""
        # Generate a unique username for each test run
        unique_id = str(uuid.uuid4())[:8]
        self.test_user = {
            'username': f'testuser_{unique_id}',
            'password': 'testpass123',
            'name': 'Test User'
        }

    def run_test_for_environment(self, test_func, env='local'):
        """Run a test function for the specified environment."""
        base_url = self.local_url if env == 'local' else self.prod_url
        try:
            test_func(base_url)
        except requests.RequestException as e:
            self.skipTest(f"Skipping {env} environment test: {str(e)}")

    def test_landing_page_endpoint(self):
        """Test landing page endpoint in both environments."""
        def test_impl(base_url):
            response = requests.get(f"{base_url}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "message": "Welcome to Odyssey"
            })

        # Test both environments
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod')

    def test_register_endpoint(self):
        """Test user registration endpoint in both environments."""
        def test_impl(base_url):
            response = requests.post(
                f"{base_url}/auth/register/",
                json=self.test_user,
                headers=self.headers
            )
            
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertIn('token', data)
            self.assertIn('user_id', data)
            self.assertEqual(data['username'], self.test_user['username'])
            self.assertEqual(data['name'], self.test_user['name'])

        # Test both environments
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod')

    def test_login_endpoint(self):
        """Test login endpoint in both environments."""
        def test_impl(base_url):
            # First register a user
            requests.post(
                f"{base_url}/auth/register/",
                json=self.test_user,
                headers=self.headers
            )
            
            # Then try to login
            login_data = {
                'username': self.test_user['username'],
                'password': self.test_user['password']
            }
            
            response = requests.post(
                f"{base_url}/auth/login/",
                json=login_data,
                headers=self.headers
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('token', data)
            self.assertIn('user_id', data)

        # Test both environments
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod')

    def test_landing_page_postauth_endpoint(self):
        """Test landing page post-auth endpoint in both environments."""
        def test_impl(base_url):
            # First register and get token
            register_response = requests.post(
                f"{base_url}/auth/register/",
                json=self.test_user,
                headers=self.headers
            )
            token = register_response.json()['token']
            
            # Add token to headers
            auth_headers = {
                **self.headers,
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(
                f"{base_url}/auth/welcome/",
                headers=auth_headers
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "message": f"Welcome back, {self.test_user['name']}"
            })

        # Test both environments
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod') 