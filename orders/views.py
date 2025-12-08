from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem
from django.db import transaction
from .utils import send_order_confirmation_email

# Create your views here.

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    
class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Create Order
        order = Order.objects.create(user=user)
        total_amount = 0
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_amount += item.product.price * item.quantity
            
        order.total_amount = total_amount
        order.save()
        
        
        # Clear Cart
        cart_items.delete()
        
        send_order_confirmation_email(user.email, order)
        
        serializers = OrderSerializer(order)
        return Response(serializers.data, status=status.HTTP_201_CREATED)