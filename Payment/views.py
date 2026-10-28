from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from Payment.models import Payment
from Cart.models import Cart
from Order.models import Order, OrderItem
from Accounts.models import CustomerProfile
import stripe



@login_required
def checkout(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = cart.cart_items.select_related('variant__product').all()

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_detail')

    address = customer.address.first()
    if not address:
        messages.error(request, 'Please add a shipping address before checkout.')
        return redirect('address_list')

    order = Order.objects.create(
        customer=customer,
        address=address,
        status='Pending',
        total_amount=Decimal('0.00'),
    )

    total_amount = Decimal('0.00')
    for cart_item in cart_items:
        product = cart_item.variant.product
        quantity = int(cart_item.quantity)
        if quantity <= 0:
            continue

        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=quantity,
        )
        total_amount += product.price * Decimal(quantity)

    order.total_amount = total_amount
    order.save(update_fields=['total_amount'])
    cart.cart_items.all().delete()

    return redirect('payment_initiate', order_id=order.pk)


@login_required
def payment_initiate(request, order_id):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    order = get_object_or_404(Order, pk=order_id, customer=customer)
    items = OrderItem.objects.filter(order=order).select_related('product')

    if not items.exists():
        messages.error(request, 'This order does not have any items.')
        return redirect('cart_detail')

    line_items = []
    for item in items:
        line_items.append(
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.product_name,
                    },
                    'unit_amount': int((item.price * Decimal('100')).quantize(Decimal('1'))),
                },
                'quantity': item.quantity,
            }
        )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('product_list')) + '?payment=success',
        cancel_url=request.build_absolute_uri(reverse('cart_detail')),
        metadata={'order_id': str(order.pk)}
    )

    Payment.objects.create(
        order=order,
        transaction_id=session.id,
        ammount=order.total_amount,
        method='Card',
        stripe_session_id=session.id,
    )

    return redirect(session.url, permanent=False)