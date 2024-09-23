# main_app/admin.py
from django.contrib import admin
from .models import *

# admin.site.register(HomeOwner)
# admin.site.register(ServiceProvider)
# admin.site.register(MaterialProvider)
admin.site.register(Community)
admin.site.register(User)
admin.site.register(ProfileGallery)

admin.site.register(SupportTickets)
admin.site.register(UserActivity)