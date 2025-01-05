"""
Vertical Authentication Testing Suite

This module implements a vertical testing approach for authentication,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import requests
import uuid
import os

User = get_user_model()

class VerticalAuthenticationTests(TestCase):
    """
    Vertical test suite for authentication that progresses from:
    1. Basic auth operations (from test_auth.py)
    2. Complete auth flows (from test_auth_flow.py)
    3. API endpoint health checks
    4. Production endpoint verification
    """
    
    def setUp(self):
        """Set up test client and base test data."""
        self.client = APIClient()
        # Generate unique username for each test run
        unique_id = str(uuid.uuid4())[:8]
        self.test_user_data = {
            'username': f'testuser_{unique_id}',
            'password': 'testpass123',
            'name': 'Test User'
        }
        # Setup URLs for endpoint tests
        self.local_url = 'http://localhost:8000'
        self.prod_url = 'https://b6kfw0mhn8.execute-api.eu-west-2.amazonaws.com/default'
        self.headers = {'Content-Type': 'application/json'}

    # Level 1: Basic Authentication Tests
    def test_1_1_landing_page(self):
        """Test landing page is accessible without auth"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Welcome to Odyssey')

    def test_1_2_register(self):
        """Test basic user registration"""
        response = self.client.post('/auth/register/', self.test_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)
        self.assertEqual(data['username'], self.test_user_data['username'])
        self.assertEqual(data['name'], self.test_user_data['name'])

    def test_1_3_login(self):
        """Test basic user login"""
        User.objects.create_user(
            username=self.test_user_data['username'],
            password=self.test_user_data['password'],
            name=self.test_user_data['name']
        )
        
        response = self.client.post('/auth/login/', {
            'username': self.test_user_data['username'],
            'password': self.test_user_data['password']
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)

    # Level 2: Complete Authentication Flow
    def test_2_1_complete_register_login_flow(self):
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
        register_response = self.client.post('/auth/register/', self.test_user_data, format='json')
        self.assertEqual(register_response.status_code, 201)
        register_data = register_response.json()
        self.assertIn('token', register_data)
        self.assertIn('user_id', register_data)
        
        # Clear any auth that might have been set
        self.client.credentials()
        
        # 3. Login with new user
        login_response = self.client.post('/auth/login/', {
            'username': self.test_user_data['username'],
            'password': self.test_user_data['password']
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
            f'Welcome back, {self.test_user_data["name"]}'
        )

    # Level 3: API Health Checks
    def test_3_1_lambda_handler_response(self):
        """Test the basic API response format"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)

    # Level 4: Production Endpoint Tests
    def run_prod_test(self, test_func):
        """Helper to run production endpoint tests with proper error handling"""
        try:
            test_func()
        except requests.RequestException:
            self.skipTest("Skipping production test - endpoint not accessible")

    def test_4_1_prod_landing_page(self):
        """Test production landing page endpoint"""
        def test_impl():
            response = requests.get(f"{self.prod_url}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Welcome to Odyssey"})
        
        self.run_prod_test(test_impl)

    def test_4_2_prod_auth_flow(self):
        """Test complete authentication flow in production"""
        def test_impl():
            # Register
            register_response = requests.post(
                f"{self.prod_url}/auth/register/",
                json=self.test_user_data,
                headers=self.headers
            )
            self.assertEqual(register_response.status_code, 201)
            token = register_response.json()['token']
            
            # Login
            login_response = requests.post(
                f"{self.prod_url}/auth/login/",
                json={
                    'username': self.test_user_data['username'],
                    'password': self.test_user_data['password']
                },
                headers=self.headers
            )
            self.assertEqual(login_response.status_code, 200)
            
            # Check protected endpoint
            auth_headers = {**self.headers, 'Authorization': f'Bearer {token}'}
            welcome_response = requests.get(
                f"{self.prod_url}/auth/welcome/",
                headers=auth_headers
            )
            self.assertEqual(welcome_response.status_code, 200)
        
        self.run_prod_test(test_impl) 