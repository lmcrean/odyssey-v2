"""
Integration tests for authentication flows.
Tests complete user journeys involving authentication.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthFlowTests(TestCase):
    """Test suite for authentication flows."""
    def setUp(self):
        """Set up test client and base data."""
        self.client = APIClient()
        self.base_user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'name': 'Test User'
        }

    def test_register_login_flow(self):
        """
        Test complete registration and login flow.
        
        Flow:
        1. Arrive on landing page
        2. Register new user
        3. Login
        4. Access protected endpoint
        5. Verify welcome message for authenticated user
        """
        # 1. Check landing page (unauthenticated)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Welcome to Odyssey')
        
        # 2. Register new user
        register_response = self.client.post('/auth/register/', self.base_user_data, format='json')
        self.assertEqual(register_response.status_code, 201)
        register_data = register_response.json()
        self.assertIn('token', register_data)
        self.assertIn('user_id', register_data)
        user_id = register_data['user_id']
        
        # Clear any auth that might have been set
        self.client.credentials()
        
        # 3. Login with new user
        login_response = self.client.post('/auth/login/', {
            'username': self.base_user_data['username'],
            'password': self.base_user_data['password']
        }, format='json')
        self.assertEqual(login_response.status_code, 200)
        login_data = login_response.json()
        self.assertIn('token', login_data)
        
        # Set token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_data["token"]}')
        
        # 4 & 5. Access protected endpoint and verify welcome message
        welcome_response = self.client.get('/auth/welcome/')
        self.assertEqual(welcome_response.status_code, 200)
        self.assertEqual(
            welcome_response.json()['message'],
            f'Welcome back, {self.base_user_data["name"]}'
        )
