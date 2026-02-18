from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product, Category, Brand
from .services import ProductService
from decimal import Decimal

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="Sony")
        self.product = Product.objects.create(
            name="PlayStation 5",
            category=self.category,
            brand=self.brand,
            price=Decimal("499.99"),
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "PlayStation 5")
        self.assertEqual(str(self.product), "PlayStation 5")
        self.assertEqual(self.product.stock, 10)

    def test_stock_update_service(self):
        updated_product = ProductService.update_stock(self.product.id, -2)
        self.assertEqual(updated_product.stock, 8)
        
        with self.assertRaises(Exception): # DRF ValidationError
            ProductService.update_stock(self.product.id, -20)

class ProductAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@test.com', password='password123')
        self.normal_user = User.objects.create_user(username='user', email='user@test.com', password='password123')
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="Sony")
        self.list_url = reverse('product-list')
        
    def test_list_products_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_admin_only(self):
        data = {
            "name": "New Product",
            "category_id": self.category.id,
            "brand_id": self.brand.id,
            "price": "99.99",
            "stock": 100
        }
        
        # Unauthorized
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Normal user (should be forbidden if we set AdminOnly for POST)
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_validation(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "name": "Invalid Price",
            "category_id": self.category.id,
            "brand_id": self.brand.id,
            "price": "-10.00",
            "stock": 10
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_MESSAGE if hasattr(status, 'HTTP_400_BAD_MESSAGE') else status.HTTP_400_BAD_REQUEST)
