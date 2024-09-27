# main_app/urls.py
from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, CategorySitemap, UserSitemap

# Define the sitemaps dictionary
sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'users': UserSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<path:category_path>', views.category_view, name='category_view'),
    path('validate', views.validate, name='validate'),
    path('register', views.register, name='register'),
    path('login', views.signin, name='login'),
    path('profile', views.profile, name='profile'),
    path('splash', views.splash, name='splash'),
    path('logout', views.signout, name='logout'),
    path('become_a_member', views.become_a_member, name='become_a_member'),
    
    path('home-owner', views.home_owner_view, name='home_owner'),
    path('service-provider', views.submit_service_provider, name='service_provider'),
    path('material-provider', views.submit_material_provider, name='submit_material_provider'),
    
    path('material-provider/<path:category_path>/<str:uid>', views.brand_info, name='brand_info'),
    path('service-provider/<path:category_path>/<str:uid>', views.user_info, name='user_info'),
    path('success', views.success_page, name='success_page'),
    path('contact', views.contact, name='contact_us'),
    path('privacy', views.privacy_policy, name='privacy_policy'),
    path('faq', views.faq, name='faq'),
    path('terms', views.terms_and_conditions, name='terms_and_conditions'),
    
    path('api/suggestions', views.suggestions, name='suggestions'),
    path('reset-password', views.reset_password, name='reset_password'),
    
    path('connect-impression/<str:brand_id>', views.connect_impression, name='connect_impression'),

    # Sitemap URL
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
