from django.core.management.base import BaseCommand
from Product.models import Category, Product, ProductVariant

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()



class Command(BaseCommand):
    help = 'Seed the database with sample product categories and products.'

    categories = [
        {'category_name': 'Electronics', 'slug': 'electronics'},
        {'category_name': 'Fashion', 'slug': 'fashion'},
        {'category_name': 'Home and Living', 'slug': 'home-and-living'},
    ]

    products = [
        {
            'product_name': 'Wireless Headphones',
            'slug': 'wireless-headphones',
            'description': 'Comfortable over-ear headphones with clear sound and long battery life.',
            'price': '79.99',
            'category': 'electronics',
        },
        {
            'product_name': 'Smart Watch',
            'slug': 'smart-watch',
            'description': 'A lightweight smartwatch for notifications, fitness tracking, and daily activity.',
            'price': '129.99',
            'category': 'electronics',
        },
        {
            'product_name': 'Classic Cotton T-Shirt',
            'slug': 'classic-cotton-t-shirt',
            'description': 'A soft, breathable cotton t-shirt with a relaxed everyday fit.',
            'price': '24.50',
            'category': 'fashion',
        },
        {
            'product_name': 'Canvas Backpack',
            'slug': 'canvas-backpack',
            'description': 'A durable backpack with a padded laptop compartment and multiple pockets.',
            'price': '54.00',
            'category': 'fashion',
        },
        {
            'product_name': 'Ceramic Coffee Mug',
            'slug': 'ceramic-coffee-mug',
            'description': 'A simple 12-ounce ceramic mug for coffee, tea, and other hot drinks.',
            'price': '12.99',
            'category': 'home-and-living',
        },
        {
            'product_name': 'Minimal Desk Lamp',
            'slug': 'minimal-desk-lamp',
            'description': 'An adjustable LED desk lamp with three brightness settings.',
            'price': '39.95',
            'category': 'home-and-living',
        },
    ]

    def handle(self, *args, **options):
        category_map = {}
        for category_data in self.categories:
            category, _ = Category.objects.update_or_create(
                slug=category_data['slug'],
                defaults={'category_name': category_data['category_name']},
            )
            category_map[category.slug] = category

        for product_data in self.products:
            product_values = {
                key: value
                for key, value in product_data.items()
                if key != 'category'
            }
            product_values['product_category'] = category_map[product_data['category']]
            product, _ = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults=product_values,
            )

            if product.slug == 'wireless-headphones':
                ProductVariant.objects.update_or_create(
                    product=product,
                    color='Black',
                    defaults={'stock': 25, 'image': ''},
                )
                ProductVariant.objects.update_or_create(
                    product=product,
                    color='White',
                    defaults={'stock': 15, 'image': ''},
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeded {len(self.categories)} categories and {len(self.products)} products.'
            )
        )