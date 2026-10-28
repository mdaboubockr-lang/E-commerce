from django.db import models
from shared.models import TimestampMixin
from Order.models import Order

# Create your models here.

class Payment(TimestampMixin):
    METHOD_CHOICES = [
        ('Card','card'),
        ('Mobile Banking','mobile banking'),
        ('Cash on Delivery','cash on delivery'),
    ]

    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=100)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=100)
    paid_at = models.DateTimeField(auto_now_add=True)
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Pyment-{self.id}"