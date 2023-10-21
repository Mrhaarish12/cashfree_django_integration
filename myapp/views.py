from django.shortcuts import render, redirect
import uuid
# from cashfree_sdk import Client  # Import Cashfree SDK
from .models import Order
from .forms import OrderForm
from django.conf import settings

def initiate_payment(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()  # Save the order

            # Access Cashfree settings from your project's settings
            cashfree_settings = settings.CASHFREE
            app_id = cashfree_settings['APP_ID']
            secret_key = cashfree_settings['SECRET_KEY']
            environment = cashfree_settings['ENV']  # 'sandbox' or 'production'

            # Generate a unique payment session ID
            payment_session_id = str(uuid.uuid4())  # Convert the UUID to a string

            # Redirect to the payment gateway view
            return render(request, 'myapp/payment_gateway.html', {
                'form': form,
                'payment_session_id': payment_session_id,
                'app_id': app_id,
                'secret_key': secret_key,
                'environment': environment,
            })

    else:
        form = OrderForm()
    return render(request, 'myapp/order_form.html', {'form': form})

def payment_gateway(request):
    return render(request, 'myapp/payment_gateway.html')

def payment_success(request):
    return render(request, 'myapp/payment_success.html')

def payment_notify(request):
    # Handle payment notification logic here
    # You can process the notification and update the order status, for example.
    return render(request, 'myapp/payment_notify.html')