from django.db import models
from Accounts.models import CustomerProfile
from Product.models import Product
from shared.models import TimestampMixin

# Create your models here.

class Review(TimestampMixin):
    RATING_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    rating = models.CharField(choices=RATING_CHOICES, max_length=2)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Review by-{self.customer.user.first_name}_{self.customer.user.last_name} on {self.product.product_name}"