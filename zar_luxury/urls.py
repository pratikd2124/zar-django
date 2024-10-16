"""
URL configuration for zar_luxury project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from main_app.sitemaps import StaticViewSitemap, CategorySitemap, BrandSitemap, ServiceProviderSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'brands': BrandSitemap,
    'service_providers': ServiceProviderSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', include('main_app.urls')),  # Include the URLs from main_app (where your views are)
    path('dashboard/',include('home.urls')),
    path('chatbot/',include('chatbot.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'