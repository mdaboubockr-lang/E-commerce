from django.db import models
from Accounts.models import CustomerProfile
from shared.models import TimestampMixin
from Product.models import ProductVariant

# Create your models here.

class Cart(TimestampMixin):
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE, related_name='carts')

    def __str__(self):
        return f"Cart-{self.id} of customer {self.customer.id}"


class CartItem(TimestampMixin):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(to=ProductVariant, on_delete=models.CASCADE, related_name='variants')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Cart Item-{self.id} of {self.cart.id}"