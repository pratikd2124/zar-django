from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    # This is for generating the full category chain (e.g., Home / Materials / Furniture)
    def get_category_hierarchy(self):
        category_hierarchy = []
        category = self
        while category:
            category_hierarchy.append(category.name)
            category = category.parent
        return "/".join(category_hierarchy[::-1])
    
    def __str__(self):
        return self.get_category_hierarchy()


class ProjectImages(models.Model):
    image = models.ImageField(upload_to='project_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

class PagesData(models.Model):
    terms_and_conditions = RichTextField(blank=True, null=True)
    privacy_policy = RichTextField(blank=True, null=True)
    faq = RichTextField(blank=True, null=True)
    guide = RichTextField(blank=True, null=True)