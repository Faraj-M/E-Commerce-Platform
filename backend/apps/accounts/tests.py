"""Accounts test suite (Unit + Integration tests requirements)."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TestUserModel(TestCase):
    """Unit tests for User model."""
    
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='+1234567890',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            country='Test Country'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.phone, '+1234567890')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class TestAuthenticationViews(TestCase):
    """Unit tests for authentication views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='existingpass'
        )
    
    def test_signup_page_loads(self):
        """Test signup page is accessible."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_creates_user(self):
        """Test user registration."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_page_loads(self):
        """Test login page is accessible."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(reverse('login'), {
            'username': 'existing',
            'password': 'existingpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_profile_requires_login(self):
        """Test profile page requires authentication."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class TestUserAPI(TestCase):
    """Integration tests for User API."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
    
    def test_me_endpoint_requires_auth(self):
        """Test /api/users/me/ requires authentication."""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_me_endpoint_works(self):
        """Test /api/users/me/ returns user data."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'apiuser')
