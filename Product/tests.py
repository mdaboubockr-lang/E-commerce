from django.test import TestCase
from django.urls import reverse

from Product.models import Category, Product


class ProductListSearchTests(TestCase):
	def setUp(self):
		category = Category.objects.create(category_name='Shoes', slug='shoes')
		Product.objects.create(
			product_name='Blue Runner',
			product_category=category,
			slug='blue-runner',
			description='Lightweight running shoes',
			price='49.99',
		)
		Product.objects.create(
			product_name='Canvas Bag',
			product_category=category,
			slug='canvas-bag',
			description='Everyday carry bag',
			price='29.99',
		)

	def test_product_list_filters_by_search_query(self):
		response = self.client.get(reverse('product_list'), {'q': 'runner'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Blue Runner')
		self.assertNotContains(response, 'Canvas Bag')
