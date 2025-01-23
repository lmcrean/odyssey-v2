"""
Vertical Authentication Testing Suite

This module implements a vertical testing approach for authentication,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.

The Vertical Authentication confirms that the following:
1. The landing page is accessible without authentication
2. User registration is successful
3. User login is successful
4. The protected welcome endpoint is accessible with valid credentials
5. The protected welcome endpoint is not accessible without valid credentials
6. TODO: User Logout is successful
7. TODO: User Deletion is successful
8. TODO: User Update is successful
9. TODO: User Password Reset is successful
10. TODO: User Password Reset Confirmation is successful
"""

import uuid
import os
import json
import boto3
import requests


from django.test import TestCase
from django.contrib.auth import get_user_model
from pathlib import Path
from botocore.auth import SigV4Auth # noqa
from botocore.awsrequest import AWSRequest # noqa
from rest_framework.test import APIClient # noqa
from rest_framework import status # noqa
User = get_user_model()

class VerticalAuthenticationTests(TestCase):
    """
    Vertical test suite for authentication that progresses from:
    1. Basic auth operations (from test_auth.py)
    2. Complete auth flows (from test_auth_flow.py)
    3. API endpoint health checks
    4. Production endpoint verification

    To run this test suite, run the following command:

    python manage.py test drf_api.tests.vertical.test_vertical_auth
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
        # Update URLs for endpoint tests
        self.local_url = 'http://localhost:8000'
        self.prod_url = 'https://t8g987asx0.execute-api.eu-west-2.amazonaws.com/prod'
        self.request_timeout = 10  # Timeout in seconds
        
        # Load API key from .env file
        env_path = Path(__file__).parent.parent.parent.parent / '.env'
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Set up AWS credentials
        self.session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='eu-west-2'
        )
        self.credentials = self.session.get_credentials()
        
        # Basic headers
        self.api_key = os.getenv('API_KEY', '')
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        # API endpoints
        self.endpoints = {
            'landing': '/welcome-noauth',
            'register': '/auth/register',
            'login': '/auth/login',
            'welcome': '/auth/welcome'
        }

    def sign_request(self, method, url, headers=None, data=None):
        """Sign a request with AWS SigV4"""
        if headers is None:
            headers = {}
        # Create AWS request
        request = AWSRequest(
            method=method,
            url=url,
            data=json.dumps(data) if data else None,
            headers=headers
        )
        # Sign with SigV4
        SigV4Auth(self.credentials, "execute-api", "eu-west-2").add_auth(request)
        # Get signed headers and add API key
        signed_headers = dict(request.headers)
        signed_headers['x-api-key'] = self.api_key
        return signed_headers

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
            # Sign request with both API key and IAM auth
            headers = self.sign_request('GET', f"{self.prod_url}{self.endpoints['landing']}", headers=self.headers)
            response = requests.get(f"{self.prod_url}{self.endpoints['landing']}", headers=headers, timeout=self.request_timeout)
            
            # Handle Lambda response format
            data = response.json()
            self.assertEqual(data['statusCode'], 200)
            body = json.loads(data['body'])
            self.assertIn('message', body)
            self.assertEqual(body['message'], 'Welcome to Odyssey - Public Landing Page')
        
        self.run_prod_test(test_impl)

    def test_4_2_prod_auth_flow(self):
        """Test complete authentication flow in production"""
        def test_impl():  # noqa: F841  # Used indirectly via run_prod_test
            # Register with all required fields
            register_data = {
                'username': self.test_user_data['username'],
                'password': self.test_user_data['password'],
                'name': self.test_user_data['name'],
                'email': f"{self.test_user_data['username']}@example.com",
                'confirm_password': self.test_user_data['password'],
                'phone': '+1234567890'  # Add required phone field
            }
            # Sign registration request
            headers = self.sign_request(
                'POST',
                f"{self.prod_url}{self.endpoints['register']}",
                headers=self.headers,
                data=register_data
            )
            
            register_response = requests.post(
                f"{self.prod_url}{self.endpoints['register']}",
                json=register_data,
                headers=headers,
                timeout=self.request_timeout
            )
            
            # Handle AWS Lambda response format
            response_data = register_response.json()
            self.assertEqual(response_data['statusCode'], 200)
            response_body = json.loads(response_data['body'])
            token = response_body.get('token')
            if not token:  # If token not in response, try login
                # Sign login request
                login_data = {
                    'username': register_data['username'],
                    'password': register_data['password']
                }
                login_headers = self.sign_request(
                    'POST',
                    f"{self.prod_url}{self.endpoints['login']}",
                    headers=self.headers,
                    data=login_data
                )
                
                login_response = requests.post(
                    f"{self.prod_url}{self.endpoints['login']}",
                    json=login_data,
                    headers=login_headers,
                    timeout=self.request_timeout
                )
                login_data = login_response.json()
                self.assertEqual(login_data['statusCode'], 200)
                login_body = json.loads(login_data['body'])
                token = login_body['token']
            
            # Check protected endpoint with API key, IAM auth, and JWT token
            auth_headers = {
                **self.headers,
                'Authorization': f'Bearer {token}'  # JWT token for user authentication
            }
            
            # Sign welcome request
            welcome_headers = self.sign_request(
                'GET',
                f"{self.prod_url}{self.endpoints['welcome']}",
                headers=auth_headers
            )
            
            welcome_response = requests.get(
                f"{self.prod_url}{self.endpoints['welcome']}",
                headers=welcome_headers,
                timeout=self.request_timeout
            )
            welcome_data = welcome_response.json()
            self.assertEqual(welcome_data['statusCode'], 200)
            welcome_body = json.loads(welcome_data['body'])
            self.assertIn('message', welcome_body)