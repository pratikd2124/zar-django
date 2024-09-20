from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

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
        return " / ".join(category_hierarchy[::-1])



class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brand_logos', blank=True, null=True)
    
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
  
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    status = models.CharField(max_length=10, default='Pending')
    # Brand can be linked to only one category in the hierarchy
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.name