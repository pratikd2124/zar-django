# main_app/admin.py
from django.contrib import admin
from .models import *

class TermsAndConditionsSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_enabled')
    list_editable = ('order', 'is_enabled')
    ordering = ('order',)

# Privacy Policy Admin
class PrivacyPolicySectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_enabled')
    list_editable = ('order', 'is_enabled')
    ordering = ('order',)

# FAQ Admin
class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_enabled')
    list_editable = ('order', 'is_enabled')
    ordering = ('order',)
    
class CustomEmailAdmin(admin.ModelAdmin):
    list_display = ('recipient_email', 'subject', 'created_at')
    search_fields = ('recipient_email', 'subject')
    ordering = ('-created_at',)

# Register the models
admin.site.register(TermsAndConditionsSection, TermsAndConditionsSectionAdmin)
admin.site.register(PrivacyPolicySection, PrivacyPolicySectionAdmin)
admin.site.register(FAQSection, FAQSectionAdmin)

admin.site.register(CustomEmail, CustomEmailAdmin)
# admin.site.register(HomeOwner)
# admin.site.register(ServiceProvider)
# admin.site.register(MaterialProvider)
admin.site.register(Community)
admin.site.register(User)
admin.site.register(ProfileGallery)
admin.site.register(ProfileInfo)

admin.site.register(SupportTickets)
admin.site.register(ContactPageDetails)
admin.site.register(ConnectImpress)