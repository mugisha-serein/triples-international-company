from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Product, Category, Brand
from .models import CartItem
from .services import CartService
from decimal import Decimal

User = get_user_model()

class CartServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='svcuser', email='svc@test.com', password='password123')
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="Sony")
        self.product = Product.objects.create(
            name="Headphones", category=self.category, brand=self.brand, price=Decimal("100.00"), stock=10
        )

    def test_add_item_success(self):
        cart_item = CartService.add_item(self.user, self.product, 2)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(CartItem.objects.count(), 1)
        
        # Add same item again
        cart_item = CartService.add_item(self.user, self.product, 3)
        self.assertEqual(cart_item.quantity, 5)

    def test_add_item_insufficient_stock(self):
        with self.assertRaises(Exception): # serializers.ValidationError
            CartService.add_item(self.user, self.product, 11)

    def test_update_item_success(self):
        cart_item = CartService.add_item(self.user, self.product, 2)
        updated_item = CartService.update_item(self.user, cart_item.id, 5)
        self.assertEqual(updated_item.quantity, 5)

    def test_remove_item(self):
        cart_item = CartService.add_item(self.user, self.product, 2)
        CartService.remove_item(self.user, cart_item.id)
        self.assertEqual(CartItem.objects.count(), 0)

class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', email='api@test.com', password='password123')
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="Sony")
        self.product = Product.objects.create(
            name="Mouse", category=self.category, brand=self.brand, price=Decimal("50.00"), stock=10
        )
        self.list_url = reverse('cart-list')
        self.add_url = reverse('cart-add')

    def test_add_to_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"product_id": self.product.id, "quantity": 2}
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_to_cart_exceeds_stock(self):
        self.client.force_authenticate(user=self.user)
        data = {"product_id": self.product.id, "quantity": 11}
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_cart_list_optimization(self):
        self.client.force_authenticate(user=self.user)
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        
        with self.assertNumQueries(4): # 1 auth, 1 count, 1 list, 1 images prefetch (from serializer)
             # Note: select_related fetches product in the list query, but nested serializers might trigger image fetch
             # We expect optimization, verifying low query count
             self.client.get(self.list_url)
