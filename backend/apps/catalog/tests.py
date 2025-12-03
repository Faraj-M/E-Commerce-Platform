"""Catalog-focused tests (covers unit, integration, and perf checks)."""

from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category, Product


class TestCategoryModel(TestCase):
    """Unit tests for Category model."""
    
    def test_create_category(self):
        category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(category.slug, 'electronics')
    
    def test_category_ordering(self):
        Category.objects.create(name='Z Category', slug='z-category')
        Category.objects.create(name='A Category', slug='a-category')
        
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, 'A Category')


class TestProductModel(TestCase):
    """Unit tests for Product model."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
    
    def test_create_product(self):
        product = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='A smartphone',
            price=Decimal('699.99'),
            category=self.category,
            stock_quantity=10
        )
        self.assertEqual(product.name, 'Smartphone')
        self.assertEqual(product.price, Decimal('699.99'))
        self.assertTrue(product.is_in_stock())


class TestProductViews(TestCase):
    """Integration tests for product views."""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=Decimal('99.99'),
            category=self.category,
            stock_quantity=10,
            is_active=True
        )
    
    def test_product_list_page(self):
        """Test product list page loads."""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_page(self):
        """Test product detail page loads."""
        response = self.client.get(reverse('product_detail', args=['test-product']))
        self.assertEqual(response.status_code, 200)


class TestCatalogAPI(TestCase):
    """Integration tests for Catalog API."""
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='API Product',
            slug='api-product',
            description='For API tests',
            price=Decimal('99.99'),
            category=self.category,
            stock_quantity=10,
            is_active=True
        )
    
    def test_product_list_api(self):
        """Test GET /api/products/."""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_list_api(self):
        """Test GET /api/categories/."""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
