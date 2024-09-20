# main_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Extending Django User model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('home_owner', 'Home Owner'),
        ('service_provider', 'Service Provider'),
        ('material_provider', 'Material Provider'),
    )
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Add related_name to avoid clash with Django's built-in User groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoid clashes with default User model
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Avoid clashes with default User model
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name='user permissions'
    )


# HomeOwner Model
class HomeOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    intrest = models.TextField()

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
