from django.db import transaction
from .models import Product, ProductImage
from rest_framework import serializers

class ProductService:
    @staticmethod
    @transaction.atomic
    def create_product(validated_data, images=None):
        """
        Creates a product and its associated images atomically.
        """
        product = Product.objects.create(**validated_data)
        
        if images:
            for image_data in images:
                ProductImage.objects.create(product=product, **image_data)
        
        return product

    @staticmethod
    @transaction.atomic
    def update_stock(product_id, quantity_change):
        """
        Thread-safe stock update logic using select_for_update.
        """
        # Lock the row for update
        product = Product.objects.select_for_update().get(id=product_id)
        
        if product.stock + quantity_change < 0:
            raise serializers.ValidationError("Insufficient stock.")
        
        product.stock += quantity_change
        product.save()
        return product

    @staticmethod
    def validate_image(image):
        """
        Basic image validation (size and format).
        """
        max_size = 5 * 1024 * 1024  # 5MB
        if image.size > max_size:
            raise serializers.ValidationError("Image file too large (max 5MB).")
        
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
        extension = image.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            raise serializers.ValidationError(f"Unsupported image format: {extension}")
        
        return image
