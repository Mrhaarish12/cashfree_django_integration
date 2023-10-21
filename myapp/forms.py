from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_id', 'currency', 'amount', 'customer_name', 'customer_email', 'customer_phone', 'order_note']
