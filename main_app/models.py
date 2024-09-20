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

class ProfileGallery(models.Model):
    image = models.ImageField(upload_to='profile_gallery')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ProjectImages(models.Model):
    image = models.ImageField(upload_to='project_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Home Owner', 'Home Owner'),
        ('Service Provider', 'Service Provider'),
        ('Material Provider', 'Material Provider'),
        ('Community User','Community User')
    )
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    
    # Home Owner Fields
    mobile = models.CharField(max_length=15)
    intrest = models.TextField(blank=True, null=True)
    
    #Service Provider Fields
    firm_name = models.CharField(max_length=100,blank=True, null=True)
    firm_address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100,blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    profile_doc = models.FileField(upload_to='profile_docs/',blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_gallery = models.ManyToManyField(ProfileGallery, blank=True,null=True)
    
    #Material Provider Fields
    brand_name = models.CharField(max_length=100,blank=True, null=True)
    company_name = models.CharField(max_length=150,blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100,blank=True, null=True)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    project_img = models.ManyToManyField(ProjectImages, blank=True,null=True)
    
    
    
    payment_status = models.CharField(max_length=100, default='pending')
    community = models.ForeignKey(Community, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.username



class SupportTickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)