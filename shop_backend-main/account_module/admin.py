from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Address)
admin.site.register(models.BankInformation)
admin.site.register(models.City)
admin.site.register(models.Province)