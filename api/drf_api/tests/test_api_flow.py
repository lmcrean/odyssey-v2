"""
Test flow for API endpoints.
Runs tests in a specific order to verify API functionality from basic to complex.
"""

import unittest
import requests
import uuid
from django.contrib.auth import get_user_model
from ..lambda_function import lambda_handler

User = get_user_model()

class APIFlowTests(unittest.TestCase):
    """Test suite for complete API flow."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environments and base data."""
        cls.local_url = 'http://localhost:8000'
        cls.prod_url = 'https://b6kfw0mhn8.execute-api.eu-west-2.amazonaws.com/default'
        cls.hello_world_url = f"{cls.prod_url}/odyssey-hello-world"
        cls.headers = {'Content-Type': 'application/json'}

    def setUp(self):
        """Set up test-specific data."""
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

    def test_01_hello_world_lambda(self):
        """Test 1: Verify Hello World Lambda function works."""
        # Test the lambda function directly
        response = lambda_handler()
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

    def test_02_hello_world_endpoint(self):
        """Test 2: Verify Hello World endpoint is accessible."""
        response = requests.get(self.hello_world_url, timeout=10.0)
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

    def test_03_landing_page(self):
        """Test 3: Verify landing page in both environments."""
        def test_impl(base_url):
            response = requests.get(f"{base_url}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "message": "Welcome to Odyssey"
            })

        # Test local first, then production
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod')

    def test_04_registration(self):
        """Test 4: Verify user registration in both environments."""
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

        # Test local first, then production
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod')

    def test_05_login(self):
        """Test 5: Verify user login in both environments."""
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

        # Test local first, then production
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod')

    def test_06_authenticated_welcome(self):
        """Test 6: Verify authenticated welcome page in both environments."""
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

        # Test local first, then production
        self.run_test_for_environment(test_impl, 'local')
        self.run_test_for_environment(test_impl, 'prod') 