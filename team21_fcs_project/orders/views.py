from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Order
from store.models import Product

import stripe, json
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
stripe.api_key = settings.STRIPE_SECRET_KEY

import logging
db_logger = logging.getLogger('db')

@login_required
def add(request):
    """
    Adds new order after creating appropriate stripe payment intent
    Returns the status of payment using which client takes the next action
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:
            if 'paymentMethodId' in data:
                product_id = data['product_id']
                product_qty = int(data['product_qty'])

                min_qty = 1
                max_qty = 10
                min_amount = 0
                max_amount = 1000000

                if product_qty < min_qty or product_qty > max_qty:
                    error_msg = "Invalid qty"
                    db_logger.error(f"User:{request.user.user_name} payment failed due to error: {error_msg}")
                    return JsonResponse({'error': error_msg})

                product = get_object_or_404(Product, id=product_id)
                product_total = product_qty*Decimal(product.price)
                order_amount = product_total # since only one product

                if order_amount < min_amount or order_amount > max_amount:
                    error_msg = "Invalid order amount"
                    db_logger.error(f"User:{request.user.user_name} payment failed due to error: {error_msg}")
                    return JsonResponse({'error': error_msg})

                # Create new PaymentIntent with a PaymentMethod ID from the client.
                intent = stripe.PaymentIntent.create(
                    amount=int(order_amount*100),
                    currency='inr',
                    payment_method=data['paymentMethodId'],
                    confirmation_method='manual',
                    confirm=True,
                )
                user_id = request.user.id
                order = Order.objects.create(user_id=user_id, 
                    product=product, 
                    quantity=product_qty, 
                    total_paid=order_amount, 
                    order_key=intent['id'], 
                    billing_status=False)

                db_logger.info(f"User: {request.user.user_name}, Email: {request.user.email}, placed order for Order ID: {order.pk}")

            elif 'paymentIntentId' in data:
                # Confirm the PaymentIntent to finalize payment after handling a required action
                # on the client.
                intent = stripe.PaymentIntent.confirm(data['paymentIntentId'])
                # After confirm, if the PaymentIntent's status is succeeded, fulfill the order.

                db_logger.info(f"User: {request.user.user_name}, Email: {request.user.email}, placed order successfully")


            return generate_response(intent, request)

        except stripe.error.CardError as e:
            db_logger.error(f"User:{request.user.user_name} payment failed due to error: {e.user_message}")
            return JsonResponse({'error': e.user_message})

        except Exception as e:
            # major error - totally unexpected
            db_logger.error(f"User:{request.user.user_name} payment failed due to error: {e.user_message}")
            return JsonResponse({'error': e})

# is login_required needed
def generate_response(intent, request):
    user = request.user
    """
    Helper function used by add post call to generate return response as per the stripe payment intent
    Refer to https://stripe.com/docs/payments/intents#intent-statuses for more details about its working
    Note: Versions of the API before 2019-02-11 show requires_source instead of requires_payment_method and requires_source_action instead of requires_action.
    """
    status = intent['status']
    if status == 'requires_action' or status == 'requires_source_action':
        # Card requires authentication
        db_logger.info(f"User:{request.user.user_name} did 3d secure payment")
        return JsonResponse({'requiresAction': True, 'paymentIntentId': intent['id'], 'clientSecret': intent['client_secret']})

    elif status == 'requires_payment_method' or status == 'requires_source':
        # Card was not properly authenticated, suggest a new payment method
        db_logger.error(f"User: {user.user_name}, card was denied")
        return JsonResponse({'error': 'Your card was denied, please provide a new payment method'})

    elif status == 'succeeded':
        # Payment is complete, authentication not required
        order_key = intent['id']
        if Order.objects.filter(order_key=order_key).exists():
            # the order exists and is paid for, so, change its status in db
            db_logger.info(f"User: {user.user_name}, Successfully placed order for item ID {order_key}")
            Order.objects.filter(order_key=order_key).update(billing_status=True)
        else:
            # order for the given successful payment_intent doesn't exist
            # shouldn't happen
            # do error handling
            db_logger.error(f"User: {user.user_name}, order failed")

        return JsonResponse({'clientSecret': intent['client_secret']})

@login_required
def user_orders(request):
    """
    returns all successful orders for the current user
    """
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return orders
