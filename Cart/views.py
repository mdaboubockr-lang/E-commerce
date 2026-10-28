from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from decimal import Decimal
from Cart.models import Cart, CartItem
from Product.models import ProductVariant
from Cart.forms import AddToCartForm, UpdateCartItemForm
from Accounts.models import CustomerProfile

# Create your views here.


def get_cart_summary_for_user(user):
    customer = get_object_or_404(CustomerProfile, user=user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    items = list(cart.cart_items.select_related('variant__product').all())

    total_price = Decimal('0.00')
    for item in items:
        item.line_total = item.variant.product.price * item.quantity
        total_price += item.line_total

    return {
        'customer': customer,
        'cart': cart,
        'items': items,
        'cart_items': items,
        'total_price': total_price,
        'cart_total': total_price,
        'cart_open': False,
    }


def redirect_back_to_cart(request, fallback_url_name='product_list'):
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or None
    if next_url:
        parsed = urlsplit(next_url)
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query_params['cart_open'] = '1'
        new_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query_params), parsed.fragment))
        return redirect(new_url)
    return redirect(fallback_url_name)


@login_required
def add_to_cart(request):
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            variant_id = form.cleaned_data['variant_id']
            quantity = form.cleaned_data['quantity']

            variant = get_object_or_404(
                ProductVariant, pk=int(variant_id)
            )

            if quantity > variant.stock:
                messages.error(
                    request=request,
                    message="Not enough stocks!"
                )

                return redirect('product_detail', pk=variant.product.pk)

            customer = get_object_or_404(CustomerProfile, user=request.user)
            cart,_ = Cart.objects.get_or_create(customer = customer)
            item,created = CartItem.objects.get_or_create(
                cart = cart,
                variant = variant,
                quantity = 0
            )

            if not created:
                item.quantity += quantity
            else:
                item.quantity += quantity

            item.save()

            messages.success(
                request,
                "Item added to cart!"
                )
            return redirect(f"{reverse('product_list')}?cart_open=1")
        messages.error(request, 'Invalid data.')
        return redirect('product_list')
    return redirect('product_list')

@login_required
def cart_detail(request):
    cart_context = get_cart_summary_for_user(request.user)
    return render(
        request=request,
        template_name='cart/cart_detail.html',
        context={
            'items': cart_context['items'],
            'total_price': cart_context['total_price'],
            'cart': cart_context['cart'],
            'cart_items': cart_context['cart_items'],
            'cart_total': cart_context['cart_total'],
        }
    )


@login_required
def update_cart_item(request, pk):
    item = get_object_or_404(
        CartItem,
        pk=pk,
        cart__customer__user=request.user,
    )
    if request.method == "POST":
        form = UpdateCartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > item.variant.stock:
                messages.error(
                    request=request,
                    message="Not enough stocks!"
                )
            elif quantity == 0:
                item.delete()
                messages.success(request, 'Item removed from cart.')
            elif quantity < 0:
                messages.error(
                    request=request,
                    message="Quantity can not be negative"
                )
            else:
                item.quantity = quantity
                item.save()
                messages.success(request, 'Cart updated.')
        else:
            messages.error(request, 'Invalid data.')
    return redirect('cart_detail')