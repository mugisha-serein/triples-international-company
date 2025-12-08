from django.urls import path
from .views import OrderListView, CheckoutView


urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('checkout/', CheckoutView.as_view(), name='order-checkout'),
]