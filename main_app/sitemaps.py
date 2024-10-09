from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, User

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        # List all static views to be included in the sitemap
        return ['home', 'contact_us', 'privacy_policy', 'faq', 'terms_and_conditions','become_a_member','service_provider_register','submit_material_provider','validate']

    def location(self, item):
        return reverse(item)

class CategorySitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        # You can customize the URL format if needed
        return reverse('category_view', args=[obj.get_category_hierarchy()])

class BrandSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        # Assuming that 'Material Provider' corresponds to a specific user type
        return User.objects.filter(type='Material Provider')

    def location(self, obj):
        # Check if the user has at least one category
        category = obj.category.first()
        if category:
            return reverse('brand_info', args=[category.get_category_hierarchy(), obj.uid])
        else:
            # Fallback to a generic brand info URL if no category is associated
            return reverse('brand_info', args=['no-category', obj.uid])

class ServiceProviderSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        # Assuming that 'Service Provider' corresponds to a specific user type
        return User.objects.filter(type='Service Provider')

    def location(self, obj):
        # Check if the user has at least one category
        category = obj.category.first()
        if category:
            return reverse('user_info', args=[category.get_category_hierarchy(), obj.uid])
        else:
            # Fallback to a generic service provider info URL if no category is associated
            return reverse('user_info', args=['no-category', obj.uid])
