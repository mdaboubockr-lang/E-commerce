from django.db import models
from Accounts.models import CustomerProfile, Address
from shared.models import TimestampMixin
from Product.models import Product

# Create your models here.

class Order(TimestampMixin):
    STATUS_CHOICES = [
        ('Pending','pending'),
        ('Paid','Paid'),
        ('Shipped', 'shipped'),
        ('Delivered', 'delivered'),
        ('Cancelled', 'cancelled'),
    ]

    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, related_name='addresses')
    status = models.CharField(choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order-{self.id}-{self.customer.user.first_name}-{self.customer.user.last_name}"


class OrderItem(TimestampMixin):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order-{self.order.id}-{self.order.customer.user.first_name}-{self.order.customer.user.last_name}"

