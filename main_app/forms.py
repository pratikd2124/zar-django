# main_app/forms.py
from django import forms
from .models import HomeOwner, ServiceProvider, MaterialProvider

class HomeOwnerForm(forms.ModelForm):
    class Meta:
        model = HomeOwner
        fields = ['name', 'mobile', 'intrest']

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['name', 'mobile', 'firm_name', 'firm_address', 'bio', 'category', 'social_links', 'profile_doc', 'profile_gallery', 'profile_pic']

class MaterialProviderForm(forms.ModelForm):
    class Meta:
        model = MaterialProvider
        fields = ['brand_name', 'company_name', 'company_address', 'contact_person', 'mobile', 'project_img', 'bio']
