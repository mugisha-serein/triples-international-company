from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Payment
from orders.models import Order
from .serializers import PaymentSerializer
import uuid 

# Create your views here.

class MakePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(order, 'payment'):
            return Response({"error": "Payment already exists for this order."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Simulate payment processing
        transaction_id = str(uuid.uuid4())
        payment_status = 'Completed'
        
        payment = Payment.objects.create(
            users=user,
            order=order,
            amount=order.total_amount,
            status=payment_status,
            transaction_id=transaction_id
        )
        
        # Update order status if payment is successful
        if payment_status == 'Completed':
            order.status = 'Processing'
            order.save()
            
        serializers = PaymentSerializer(payment)
        return Response(serializers.data, status=status.HTTP_201_CREATED)