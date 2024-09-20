from django.contrib import admin

# Register your models here.
from .models import Category, Brand

admin.site.register(Category)
admin.site.register(Brand)