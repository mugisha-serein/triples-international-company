from django.urls import path
from .views import *

urlpatterns = [
    path('', CartItemListView.as_view(), name='cart-list'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('update/<int:item_id>/', CartUpdateView.as_view(), name='cart-update'),
    path('remove/<int:item_id>/', CartRemoveView.as_view(), name='cart-remove'),
]
