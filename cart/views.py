from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from products.models import Product
from .services import CartService

# Create your views here.

## List Current User's Cart
class CartItemListView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'cart_operations'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def get_serializer_context(self):
        return {'product_queryset': Product.objects.filter(is_active=True)}
    
    
## Add Item to Cart
class CartAddView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'product_queryset': Product.objects.filter(is_active=True)}

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        
        # Use Service
        CartService.add_item(user, product, quantity)
      
      
## Update Item Quantity in Cart   
class CartUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'product_queryset': Product.objects.filter(is_active=True)}
    

    def perform_update(self, serializer):
        CartService.update_item(self.request.user, serializer.instance.id, serializer.validated_data['quantity'])

## Remove Item from Cart
class CartRemoveView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        CartService.remove_item(self.request.user, instance.id)