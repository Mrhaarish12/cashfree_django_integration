from django.shortcuts import render, redirect
import uuid
import requests
from .models import Order
from .forms import OrderForm
from django.conf import settings
from django.utils import timezone
import pytz

def format_expiry_time(order_expiry_time):
    india_timezone = pytz.timezone("Asia/Kolkata")
    current_time = order_expiry_time.astimezone(india_timezone)
    offset = current_time.strftime('%z')
    formatted_offset = f'{offset[:-2]}:{offset[-2:]}'  # Add the colon between hours and minutes
    formatted_time = current_time.strftime(f'%Y-%m-%dT%H:%M:%S{formatted_offset}')
    return formatted_time


def initiate_payment(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()  # Save the order
            print(order)
            # Access Cashfree settings from your project's settings
            cashfree_settings = settings.CASHFREE
            app_id = cashfree_settings['APP_ID']
            secret_key = cashfree_settings['SECRET_KEY']
            environment = cashfree_settings['ENV']  # 'sandbox' or 'production'

            # Extract customer information
            customer_name = form.cleaned_data['customer_name']
            customer_email = form.cleaned_data['customer_email']
            customer_phone = form.cleaned_data['customer_phone']
            order_note = form.cleaned_data['order_note']

            # Generate a unique payment session ID
            payment_session_id = str(uuid.uuid4())  # Convert the UUID to a string
            india_timezone = pytz.timezone("Asia/Kolkata")
            order_expiry_time = timezone.now() + timezone.timedelta(minutes=20)
            print(order_expiry_time)
            formatted_expiry_time = format_expiry_time(order_expiry_time)
            print(formatted_expiry_time)
            # Make a request to Cashfree API to obtain the session ID
            cashfree_api_url = "https://sandbox.cashfree.com/pg/orders"
            headers = {
                "accept": "application/json",
                "x-api-version": "2022-09-01",
                "content-type": "application/json",
                "x-client-id": app_id,
                "x-client-secret": secret_key
            }
            print(headers)
            data = {
                "customer_details": {
                    "customer_id": str(order.customer_id),  # Use the auto-incremented customer_id
                    "customer_email": customer_email,
                    "customer_phone": customer_phone,
                    "customer_name": customer_name
                },
                "order_id": order.order_id,
                "order_amount": float(order.amount),  # Convert the amount to a float
                "order_currency": order.currency,
                "order_expiry_time": formatted_expiry_time,  # Format the expiry time
                "order_note": order_note,
            }
            print(data)
            response = requests.post(cashfree_api_url, json=data, headers=headers)
            print(response)
            if response.status_code == 200:
                # Extract session ID from the response
                session_id = response.json().get('payment_session_id')
                print(session_id)
                return render(request, 'myapp/payment_gateway.html', {
                    'form': form,
                    'payment_session_id': session_id,
                    'app_id': app_id,
                    'secret_key': secret_key,
                    'environment': environment,
                })
            elif response.status_code == 400:
                error_message = response.json().get('message')
                print(f"API Error: {error_message}")
    
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
