from django.urls import path
from . import views

urlpatterns = [
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-gateway/', views.payment_gateway, name='payment_gateway'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-notify/', views.payment_notify, name='payment_notify'),


]
