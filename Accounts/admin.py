from django.contrib import admin
from Accounts.models import CustomerProfile, Address

# Register your models here.

admin.site.register(CustomerProfile)
admin.site.register(Address)