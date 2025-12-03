"""Payments test harness (unit tests + Stripe webhook integration)."""

import json
from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch
from rest_framework.test import APIClient
from apps.catalog.models import Category, Product
from apps.orders.models import Order
from .models import Payment

User = get_user_model()


class TestPaymentModel(TestCase):
    """Unit tests for Payment model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='payuser',
            email='pay@example.com',
            password='paypass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('99.99'),
            shipping_address='123 Pay St',
            shipping_city='Pay City',
            shipping_postal_code='12345',
            shipping_country='Pay Country'
        )
    
    def test_create_payment(self):
        payment = Payment.objects.create(
            order=self.order,
            stripe_payment_intent_id='pi_test_123',
            amount=self.order.total_amount,
            status='pending'
        )
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.status, 'pending')


class TestPaymentViews(TestCase):
    """Integration tests for payment views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='payview',
            email='payview@example.com',
            password='payview123'
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('59.99'),
            shipping_address='123 View St',
            shipping_city='View City',
            shipping_postal_code='12345',
            shipping_country='View Country'
        )
    
    def test_payment_create_requires_login(self):
        """Test payment creation requires authentication."""
        response = self.client.get(reverse('payment_create', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class TestStripeWebhook(TestCase):
    """Tests for Stripe webhook integration."""
    
    def test_stripe_webhook_endpoint_exists(self):
        """Test Stripe webhook endpoint is accessible."""
        client = Client()
        response = client.post(reverse('stripe_webhook'))
        # Should return some response (400 for missing signature, etc.)
        self.assertIn(response.status_code, [200, 400, 403])


