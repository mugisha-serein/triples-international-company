from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import CartItem
from django.db import transaction
from django.db.models import Prefetch
from .utils import send_order_confirmation_email

# Create your views here.

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related(
                    'product',
                    'product__category',
                    'product__brand'
                ).prefetch_related('product__images')
            )
        ).order_by('-created_at')
    
    
class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'checkout_attempt'

    def post(self, request, *args, **kwargs):
        from .services import OrderService
        
        try:
            order = OrderService.process_checkout(request.user)
        except Exception as e:
            # If it's a validation error from service, re-raise or handle
            # check if it is a DRF ValidationError
            if hasattr(e, 'detail'):
                 return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            raise e

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)