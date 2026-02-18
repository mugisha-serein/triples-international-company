from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Product, Category, Brand
from cart.models import CartItem
from .models import Order, OrderItem
from .services import OrderService
from decimal import Decimal

User = get_user_model()

class OrderServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='srvuser', email='srv@test.com', password='password123')
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="Sony")
        self.product = Product.objects.create(
            name="PS5", category=self.category, brand=self.brand, price=Decimal("500.00"), stock=10
        )
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

    def test_process_checkout_success(self):
        order = OrderService.process_checkout(self.user)
        
        self.assertEqual(order.total_amount, Decimal("1000.00"))
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        
        # Verify stock deduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        
        # Verify cart cleared
        self.assertEqual(CartItem.objects.count(), 0)

    def test_process_checkout_insufficient_stock(self):
        # Set stock lower than cart quantity
        self.product.stock = 1
        self.product.save()
        
        with self.assertRaises(Exception): # serializers.ValidationError
            OrderService.process_checkout(self.user)
            
        # Verify no order created
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(self.product.stock, 1)

class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', email='api@test.com', password='password123')
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="Sony")
        self.product = Product.objects.create(
            name="PS5", category=self.category, brand=self.brand, price=Decimal("500.00"), stock=10
        )
        self.checkout_url = reverse('order-checkout')
        self.list_url = reverse('order-list')

    def test_checkout_authenticated(self):
        self.client.force_authenticate(user=self.user)
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        
        response = self.client.post(self.checkout_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_checkout_empty_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.checkout_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_optimization(self):
        self.client.force_authenticate(user=self.user)
        # Create an order manually to test list
        order = Order.objects.create(user=self.user, total_amount=Decimal("500.00"))
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)
        
        with self.assertNumQueries(3): # Optimized: 1. Orders, 2. Items+Products+Cat+Brand, 3. Images
             response = self.client.get(self.list_url)
             self.assertEqual(response.status_code, status.HTTP_200_OK)
