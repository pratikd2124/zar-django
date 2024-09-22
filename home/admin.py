from django.contrib import admin

# Register your models here.
from .models import Category,PagesData
admin.site.register(PagesData)

admin.site.register(Category)
# admin.site.register(Brand)