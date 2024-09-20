# main_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
# Extending Django User model

class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a unique 6-digit code
            self.code = self.generate_unique_code()
        super(Community, self).save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            code = str(random.randint(100000, 999999))
            if not Community.objects.filter(code=code).exists():
                return code
    
    
    # Add any other fields specific to the community

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('home_owner', 'Home Owner'),
        ('service_provider', 'Service Provider'),
        ('material_provider', 'Material Provider'),
    )
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    community = models.ForeignKey(Community, on_delete=models.CASCADE,blank=True, null=True)
   


# HomeOwner Model
class HomeOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    intrest = models.TextField()
    payment_status = models.CharField(max_length=100, default='pending')
    
    
# ServiceProvider Model
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    firm_name = models.CharField(max_length=150)
    firm_address = models.TextField()
    bio = models.TextField()
    category = models.CharField(max_length=100)
    social_links = models.JSONField()
    profile_doc = models.FileField(upload_to='profile_docs/')
    profile_gallery = models.ImageField(upload_to='profile_gallery/', null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    payment_status = models.CharField(max_length=100, default='pending')

# MaterialProvider Model
class MaterialProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    company_address = models.TextField()
    contact_person = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    project_img = models.ImageField(upload_to='project_images/', null=True, blank=True)
    bio = models.TextField()
    payment_status = models.CharField(max_length=100, default='pending')



class SupportTickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)