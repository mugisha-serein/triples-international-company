from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from orders.models import Order
from .models import Payment
from .services import PaymentService
from decimal import Decimal

User = get_user_model()

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='payuser', email='pay@test.com', password='password123')
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("150.00"),
            status='Pending'
        )

    def test_payment_creation(self):
        payment = Payment.objects.create(
            users=self.user,
            order=self.order,
            amount=self.order.total_amount,
            status='COMPLETED',
            transaction_id='test-trans-123'
        )
        self.assertEqual(payment.amount, Decimal("150.00"))
        self.assertEqual(payment.status, 'COMPLETED')
        self.assertIn('Payment for Order', str(payment))

class PaymentServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='srvuser', email='srv@test.com', password='password123')
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("200.00"),
            status='Pending'
        )

    def test_process_payment_success(self):
        payment = PaymentService.process_payment(self.user, self.order.id)
        self.assertEqual(payment.status, 'COMPLETED')
        
        # Verify order status update
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Processing')

    def test_prevent_double_payment(self):
        PaymentService.process_payment(self.user, self.order.id)
        
        with self.assertRaises(Exception): # serializers.ValidationError
            PaymentService.process_payment(self.user, self.order.id)

class PaymentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', email='api@test.com', password='password123')
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            status='Pending'
        )
        self.url = reverse('make-payment')

    def test_make_payment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"order_id": self.order.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'COMPLETED')

    def test_make_payment_unauthorized(self):
        data = {"order_id": self.order.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
