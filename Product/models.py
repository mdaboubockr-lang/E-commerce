from django.db import models
from shared.models import TimestampMixin

# Create your models here.

class Category(TimestampMixin):
    category_name  = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category_name


class Product(TimestampMixin):
    product_name = models.CharField(max_length=200)
    product_category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='Product')
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_product_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.product_name


class Product_image(TimestampMixin):
    image = models.ImageField(upload_to='products/images')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"image for {self.product.product_name}"


class ProductVariant(TimestampMixin):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images')
    color = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.product_name
    
