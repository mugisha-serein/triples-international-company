from rest_framework import serializers
from .models import CartItem
from products.models import Product

class CartService:
    @staticmethod
    def add_item(user, product, quantity):
        """
        Adds item to cart with stock validation.
        """
        if quantity <= 0:
             raise serializers.ValidationError("Quantity must be positive.")

        if product.stock < quantity:
            raise serializers.ValidationError(f"Insufficient stock. Available: {product.stock}")

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

        if not created:
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                 raise serializers.ValidationError(f"Cannot add {quantity}. Resulting total {new_quantity} exceeds stock {product.stock}.")
            
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
        return cart_item

    @staticmethod
    def update_item(user, item_id, quantity):
        """
        Updates item quantity with stock validation.
        """
        try:
            cart_item = CartItem.objects.select_related('product').get(id=item_id, user=user)
        except CartItem.DoesNotExist:
            raise serializers.ValidationError("Item not found in cart.")

        if quantity <= 0:
             raise serializers.ValidationError("Quantity must be positive.")

        if cart_item.product.stock < quantity:
            raise serializers.ValidationError(f"Insufficient stock. Available: {cart_item.product.stock}")

        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    @staticmethod
    def remove_item(user, item_id):
        """
        Removes item from cart.
        """
        deleted_count, _ = CartItem.objects.filter(id=item_id, user=user).delete()
        if deleted_count == 0:
             raise serializers.ValidationError("Item not found in cart.")
