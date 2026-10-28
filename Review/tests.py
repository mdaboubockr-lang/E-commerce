from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from Accounts.models import CustomerProfile
from Product.models import Category, Product
from Review.models import Review


class ReviewWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='secret123',
            first_name='Jane',
            last_name='Doe',
        )
        self.profile = CustomerProfile.objects.create(user=self.user)
        self.category = Category.objects.create(category_name='Groceries', slug='groceries')
        self.product = Product.objects.create(
            product_name='Test Rice',
            product_category=self.category,
            slug='test-rice',
            description='A rice product for review testing.',
            price='10.00',
        )

    def test_customer_can_submit_review(self):
        self.client.login(username='reviewer', password='secret123')

        response = self.client.post(
            reverse('review_create', args=[self.product.slug]),
            {'rating': '5', 'comment': 'Excellent product!'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(product=self.product, customer=self.profile).exists())
        self.assertContains(response, 'Excellent product!')
