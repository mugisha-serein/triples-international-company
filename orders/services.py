from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import CartItem
from products.models import Product
from .utils import send_order_confirmation_email

class OrderService:
    @staticmethod
    @transaction.atomic
    def process_checkout(user):
        """
        Processes order checkout atomically with stock concurrency handling.
        """
        cart_items = CartItem.objects.filter(user=user).select_related('product')

        if not cart_items.exists():
            raise serializers.ValidationError({"detail": "Cart is empty."})

        # Create Order first
        order = Order.objects.create(user=user)
        total_amount = 0
        
        for item in cart_items:
            # Lock the product row for update to prevent race conditions during checkout
            product = Product.objects.select_for_update().get(id=item.product.id)
            
            if product.stock < item.quantity:
                raise serializers.ValidationError({
                    "detail": f"Insufficient stock for {product.name}. Available: {product.stock}"
                })

            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )
            
            # Decrement stock
            product.stock -= item.quantity
            product.save()
            
            total_amount += product.price * item.quantity
            
        order.total_amount = total_amount
        order.save()
        
        # Clear Cart
        cart_items.delete()
        
        # Trigger notification
        try:
            send_order_confirmation_email(user.email, order)
        except Exception:
            # Log error but don't fail checkout
            pass
            
        return order
