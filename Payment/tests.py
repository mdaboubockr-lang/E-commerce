from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from Accounts.models import Address, CustomerProfile
from Cart.models import Cart, CartItem
from Order.models import Order, OrderItem
from Product.models import Category, Product, ProductVariant


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='secret123',
        )
        self.customer = CustomerProfile.objects.create(user=self.user, phone='1234567890')
        self.address = Address.objects.create(
            country='USA',
            city='New York',
            postal_code='10001',
            street='Main Street 1',
        )
        self.customer.address.add(self.address)

        self.category = Category.objects.create(category_name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            product_name='Headphones',
            product_category=self.category,
            slug='headphones',
            description='Wireless headphones',
            price=Decimal('99.99'),
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            image='products/images/default.png',
            color='Black',
            stock=10,
        )
        self.cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=self.cart, variant=self.variant, quantity=Decimal('1'))

    def test_checkout_creates_order_and_redirects_to_payment_initiate(self):
        self.client.login(username='buyer', password='secret123')

        response = self.client.post(reverse('checkout'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.address, self.address)
        self.assertEqual(order.total_amount, Decimal('99.99'))
        self.assertEqual(OrderItem.objects.filter(order=order).count(), 1)
        self.assertRedirects(response, reverse('payment_initiate', args=[order.pk]))
