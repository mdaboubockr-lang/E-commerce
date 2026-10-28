from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    street = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country} - {self.postal_code}"

class CustomerProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/profiles/',  null=True, blank=True)
    address = models.ManyToManyField(to=Address, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"