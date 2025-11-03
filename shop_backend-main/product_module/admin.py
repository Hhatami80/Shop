from django.contrib import admin
from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.Brand)
admin.site.register(models.ProductComment)
admin.site.register(models.ProductGallery)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductProperty)
admin.site.register(models.CategoryBanner)
