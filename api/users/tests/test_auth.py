from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'name': 'Test User'
        }
        
    def test_landing_page(self):
        """Test landing page is accessible without auth"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Welcome to Odyssey')
        
    def test_register(self):
        """Test user registration"""
        response = self.client.post('/auth/register/', self.test_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)
        self.assertEqual(data['username'], self.test_user_data['username'])
        self.assertEqual(data['name'], self.test_user_data['name'])
        
    def test_login(self):
        """Test user login"""
        # Create user first
        User.objects.create_user(
            username=self.test_user_data['username'],
            password=self.test_user_data['password'],
            name=self.test_user_data['name']
        )
        
        # Try to login
        response = self.client.post('/auth/login/', {
            'username': self.test_user_data['username'],
            'password': self.test_user_data['password']
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('user_id', data)
        
    def test_welcome_auth(self):
        """Test authenticated welcome message"""
        # Create and authenticate user
        user = User.objects.create_user(
            username=self.test_user_data['username'],
            password=self.test_user_data['password'],
            name=self.test_user_data['name']
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/auth/welcome/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], f'Welcome back, {self.test_user_data["name"]}')
