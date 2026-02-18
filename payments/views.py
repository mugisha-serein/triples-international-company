from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Payment
from orders.models import Order
from .serializers import PaymentSerializer
import uuid 

from .services import PaymentService

# Create your views here.

class MakePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'payment_attempt'

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        
        if not order_id:
            return Response({"error": "order_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # All logic (locking, validation, creation) moved to Service
        payment = PaymentService.process_payment(request.user, order_id)
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)