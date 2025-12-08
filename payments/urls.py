from django.urls import path
from . import views


urlpatterns = [
    path('make/', views.MakePaymentView.as_view(), name='make-payment'),
]