from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

class Order(models.Model):
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupees'),
        ('USD', 'US Dollars'),
        # Add more currency choices as needed
    ]

    order_id = models.CharField(max_length=100, validators=[MinLengthValidator(limit_value=3)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer_id = models.IntegerField(default=100)  # Default value for customer_id
    customer_name = models.CharField(max_length=50, default='null')
    customer_email = models.EmailField(max_length=50, default='null')
    customer_phone = models.CharField(max_length=15, default='null')
    order_expiry_time = models.DateTimeField(default=timezone.now)
    order_note = models.TextField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only increment when creating a new object
            latest_order = Order.objects.latest('customer_id')
            self.customer_id = latest_order.customer_id + 1
        super().save(*args, **kwargs)
