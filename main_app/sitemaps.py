# main_app/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Category, User  # Assuming these models exist

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages like home, contact, privacy, etc."""
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'contact_us', 'privacy_policy', 'terms_and_conditions', 'faq']

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    """Sitemap for all categories."""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Assuming Category model has `updated_at` field


class UserSitemap(Sitemap):
    """Sitemap for user profiles (e.g., service and material providers)."""
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return User.objects.filter(is_active=True, payment_status='Success')

    def lastmod(self, obj):
        return obj.updated_at  # Assuming User model has `updated_at` field

    def location(self, obj):
        # Generate dynamic URLs for users
        if obj.user_type == 'Service Provider':
            return reverse('user_info', kwargs={'category_path': obj.category.get_slugified_hierarchy(), 'uid': obj.id})
        elif obj.user_type == 'Material Provider':
            return reverse('brand_info', kwargs={'category_path': obj.category.get_slugified_hierarchy(), 'uid': obj.id})
