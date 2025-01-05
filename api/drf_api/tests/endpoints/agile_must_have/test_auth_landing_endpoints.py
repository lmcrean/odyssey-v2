"""
Tests for authentication-related API endpoints.
Verifies endpoint health and response formats.
"""

import unittest
import requests
import os
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthEndpointTests(unittest.TestCase):
    """Test suite for auth endpoints."""
    def setUp(self):
        """Set up base URLs and test data."""
        self.base_url = os.getenv('API_URL', 'http://localhost:8000')
        self.headers = {'Content-Type': 'application/json'}
        self.test_user = {
            'username': 'testuser',
            'password': 'testpass123',
            'name': 'Test User'
        }

    def test_landing_page_endpoint(self):
        """Test landing page endpoint."""
        response = requests.get(f"{self.base_url}/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "Welcome to Odyssey"
        })

    def test_register_endpoint(self):
        """Test user registration endpoint."""
        response = requests.post(
            f"{self.base_url}/auth/register/",
            json=self.test_user,
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)
        self.assertEqual(data['username'], self.test_user['username'])
        self.assertEqual(data['name'], self.test_user['name'])

    def test_login_endpoint(self):
        """Test login endpoint."""
        # First register a user
        requests.post(
            f"{self.base_url}/auth/register/",
            json=self.test_user,
            headers=self.headers
        )
        
        # Then try to login
        login_data = {
            'username': self.test_user['username'],
            'password': self.test_user['password']
        }
        
        response = requests.post(
            f"{self.base_url}/auth/login/",
            json=login_data,
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)

    def test_landing_page_postauth_endpoint(self):
        """Test landing page post-auth endpoint."""
        # First register and get token
        register_response = requests.post(
            f"{self.base_url}/auth/register/",
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
            f"{self.base_url}/auth/welcome/",
            headers=auth_headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": f"Welcome back, {self.test_user['name']}"
        }) 