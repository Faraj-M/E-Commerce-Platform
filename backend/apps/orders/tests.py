"""Orders test suite (unit, integration, and webhook flow tests)."""

from django.test import TestCase, Client
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from apps.catalog.models import Category, Product
from .models import Order, OrderItem

User = get_user_model()


class TestOrderModel(TestCase):
    """Unit tests for Order model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('199.98'),
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_postal_code='12345',
            shipping_country='Test Country'
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')


class TestCartViews(TestCase):
    """Integration tests for cart views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='cartuser',
            email='cart@example.com',
            password='cartpass123'
        )
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='Cart Product',
            slug='cart-product',
            description='For cart',
            price=Decimal('49.99'),
            category=self.category,
            stock_quantity=10,
            is_active=True
        )
    
    def test_cart_page_loads(self):
        """Test cart page loads."""
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
    
    def test_checkout_requires_login(self):
        """Test checkout requires authentication."""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_order_list_requires_login(self):
        """Test order list requires authentication."""
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class TestOrderAPI(TestCase):
    """Integration tests for Order API."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='orderuser',
            email='order@example.com',
            password='orderpass123'
        )
        
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('99.99'),
            shipping_address='123 API St',
            shipping_city='API City',
            shipping_postal_code='12345',
            shipping_country='API Country'
        )
    
    def test_order_list_api(self):
        """Test GET /api/orders/."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
