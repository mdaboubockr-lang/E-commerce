from decimal import Decimal
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from Product.models import Category, Product, ProductVariant

CATEGORIES = [
    ('Fruits & Vegetables','fruits-vegetables'),('Dairy & Eggs','dairy-eggs'),('Beverages','beverages'),
    ('Snacks & Munchies','snacks-munchies'),('Staples','staples'),('Personal Care','personal-care'),
    ('Household','household'),('Baby Care','baby-care'),('Bakery','bakery'),('Meat & Fish','meat-fish'),
    ('Frozen Foods','frozen-foods'),('Health & Wellness','health-wellness'),('Pet Care','pet-care'),
    ('Organic Products','organic-products'),('International Foods','international-foods')]

PRODUCTS = [
 ('Soybean Oil 1L','beverages',270),('Brown Rice 1kg','staples',230),('Rice Minniket 5kg','staples',520),
 ('Rice 28 5kg','staples',430),('Dano Full Cream Milk Powder 1kg','dairy-eggs',850),('Dano Full Cream Milk Powder 500gm','dairy-eggs',440),
 ('Diploma Full Cream Milk Powder 1kg','dairy-eggs',780),('Marks Full Cream Milk Powder 500gm','dairy-eggs',390),('Nestle Nido 350gm','dairy-eggs',360),
 ('Brown Eggs Pack of 12','dairy-eggs',210),('Egg Loose 12pcs','dairy-eggs',165),('Chinigura Rice 1kg','staples',190),
 ('Horlicks Lite 400gm','health-wellness',390),('Coca Cola 1.75L','beverages',180),('7Up 1.75L','beverages',180),
 ('Toilet Tissue White','household',180),('Non-Dairy Whip Topping 1L','dairy-eggs',520),('Green Apple Drink 250ml','beverages',45),
 ('Mosur Dal 1kg','staples',150),('Soybean Oil 5L','staples',880),('Ginger Local 1kg','fruits-vegetables',220),
 ('Garlic Local 1kg','fruits-vegetables',260),('Cardamom 25gm','staples',180),('Cardamom 50gm','staples',330),
 ('Cumin 200gm','staples',190),('Raisins 200gm','staples',240),('Bay Leaves 50gm','staples',65),('Cloves 50gm','staples',130),
 ('Cinnamon 200gm','staples',170),('Fresh Banana 1kg','fruits-vegetables',120),('Fresh Tomato 1kg','fruits-vegetables',135),
 ('Fresh Potato 1kg','fruits-vegetables',95),('Fresh Apple 1kg','fruits-vegetables',240),('Fresh Carrot 1kg','fruits-vegetables',110),
 ('Potato Chips 100gm','snacks-munchies',70),('Corn Flakes 250gm','snacks-munchies',175),('Peanut Butter 340gm','snacks-munchies',295),
 ('Laundry Liquid 1L','household',320),('Baby Care Lotion 200ml','baby-care',280),('Bread Large 500gm','bakery',90),
 ('Fresh Chicken 1kg','meat-fish',390),('Frozen Mixed Vegetables 500gm','frozen-foods',250),('Multivitamin 30 tablets','health-wellness',450),
 ('Organic Honey 500gm','organic-products',520),('International Pasta 500gm','international-foods',240),('Pet Food 1kg','pet-care',390),
]

IMAGE_BY_CATEGORY = {
 'fruits-vegetables':'products/images/product-banana.jpg','dairy-eggs':'products/images/product-milk.jpg','beverages':'products/images/product-oil.jpg',
 'snacks-munchies':'products/images/product-potato.jpg','staples':'products/images/product-rice.jpg','personal-care':'products/images/product-milk.jpg',
 'household':'products/images/product-oil.jpg','baby-care':'products/images/product-milk.jpg','bakery':'products/images/product-rice.jpg','meat-fish':'products/images/product-meat.jpg',
 'frozen-foods':'products/images/product-frozen.jpg','health-wellness':'products/images/product-apple.jpg','pet-care':'products/images/product-potato.jpg',
 'organic-products':'products/images/product-apple.jpg','international-foods':'products/images/product-rice.jpg'}

class Command(BaseCommand):
    help = 'Seed FreshMart grocery categories, products and cart-ready variants.'
    def handle(self,*args,**kwargs):
        cats={}
        for name,slug in CATEGORIES:
            cats[slug]=Category.objects.update_or_create(slug=slug, defaults={'category_name':name})[0]
        for number,(name,cat_slug,price) in enumerate(PRODUCTS,1):
            product=Product.objects.update_or_create(slug=f'freshmart-{number}-{slugify(name)}', defaults={'product_name':name,'product_category':cats[cat_slug],'description':f'Fresh, quality {name} selected for everyday shopping.','price':Decimal(str(price))})[0]
            if not product.productvariant_set.exists():
                ProductVariant.objects.create(product=product,color='Standard',stock=30,image=IMAGE_BY_CATEGORY.get(cat_slug,'products/images/product-banana.jpg'))
        self.stdout.write(self.style.SUCCESS(f'FreshMart catalog ready: {len(CATEGORIES)} categories and {len(PRODUCTS)} products.'))
