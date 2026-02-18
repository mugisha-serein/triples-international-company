import uuid
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Payment
from orders.models import Order

class PaymentService:
    @staticmethod
    @transaction.atomic
    def process_payment(user, order_id):
        """
        Processes a payment with race condition prevention using select_for_update.
        """
        try:
            # Lock the order record to prevent concurrent payment attempts
            order = Order.objects.select_for_update().get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError({"error": "Order not found or access denied."})

        # Check if payment already exists
        if Payment.objects.filter(order=order).exists():
            raise serializers.ValidationError({"error": "Payment already exists for this order."})

        # Validate order state (e.g., only Pending orders can be paid)
        if order.status != 'Pending':
             raise serializers.ValidationError({"error": f"Cannot pay for order in '{order.status}' status."})

        # Simulate external payment gateway call
        transaction_id = str(uuid.uuid4())
        payment_status = 'COMPLETED'  # In real world, this comes from the gateway

        # Create Payment record
        payment = Payment.objects.create(
            users=user,
            order=order,
            amount=order.total_amount,
            status=payment_status,
            transaction_id=transaction_id
        )

        # Update order status
        if payment_status == 'COMPLETED':
            order.status = 'Processing'
            order.save()

        return payment
