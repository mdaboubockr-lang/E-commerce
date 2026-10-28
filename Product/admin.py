from django.contrib import admin
from Product.models import Category, Product, Product_image, ProductVariant

# Register your models here.

admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
	model = Product_image
	extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductImageInline]


admin.site.register(Product_image)
admin.site.register(ProductVariant)