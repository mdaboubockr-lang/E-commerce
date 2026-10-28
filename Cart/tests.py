from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from Accounts.models import CustomerProfile
from Cart.models import Cart
from Product.models import Category, Product, ProductVariant


class AddToCartSideCartTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='secret123',
        )
        self.customer = CustomerProfile.objects.create(user=self.user, phone='1234567890')
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

    def test_add_to_cart_redirects_back_to_product_with_cart_sidebar_open(self):
        self.client.login(username='buyer', password='secret123')

        response = self.client.post(
            reverse('add_to_cart'),
            {'variant_id': self.variant.pk, 'quantity': 1, 'next': reverse('product_detail', args=[self.product.pk])},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(f"{reverse('product_detail', args=[self.product.pk])}?cart_open=1"))
        self.assertEqual(Cart.objects.filter(customer=self.customer).count(), 1)
