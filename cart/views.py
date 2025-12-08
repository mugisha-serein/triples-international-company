from rest_framework import generics, permissions
from .models import CartItem
from .serializer import CartItemSerializer
from products.models import Product

# Create your views here.

## List Current User's Cart
class CartItemListView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

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
        
        # Update quantity if item already exists
        cart_item, create = CartItem.objects.get_or_create(user=user, product=product)
        if not create:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            serializer.save(user=user)
      
      
## Update Item Quantity in Cart   
class CartUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'item_id'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'product_queryset': Product.objects.filter(is_active=True)}
    

## Remove Item from Cart
class CartRemoveView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'item_id'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)