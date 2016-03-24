from django.contrib import admin

# Register your models here.
from .models import products, ProductImage, Variation, Category, productfeatured
admin.site.register(products)
admin.site.register(ProductImage)
admin.site.register(Variation)

admin.site.register(Category)
admin.site.register(productfeatured)