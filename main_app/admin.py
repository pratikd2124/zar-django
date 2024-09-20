# main_app/admin.py
from django.contrib import admin
from .models import HomeOwner, ServiceProvider, MaterialProvider

admin.site.register(HomeOwner)
admin.site.register(ServiceProvider)
admin.site.register(MaterialProvider)
