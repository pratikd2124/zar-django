# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<str:category_name>', views.category_view, name='category_view'),

    path('validate',views.validate,name='validate'),
    path('register',views.register,name='register'),
    path('login',views.signin,name='login'),
    path('profile',views.profile,name='profile'),
    path('splash',views.splash,name='splash'),
    path('logout',views.signout,name='logout'),
    path('become_a_member',views.become_a_member,name='become_a_member'),
    
    path('home-owner', views.home_owner_view, name='home_owner'),
    path('service-provider', views.submit_service_provider, name='service_provider'),
    path('material-provider', views.submit_material_provider, name='submit_material_provider'),
    
    
    path('material-provider/<str:category>/<str:uid>', views.brand_info, name='brand_info'),
    path('service-provider/<str:category>/<str:uid>', views.user_info, name='user_info'),
    path('success', views.success_page, name='success_page'),
    path('contact',views.contact,name='contact_us'),
    path('privacy-policy',views.privacy_policy,name='privacy_policy'),
    path('FAQ',views.faq,name='faq'),
    path('terms-and-conditions',views.terms_and_conditions,name='terms_and_conditions'),
    
    
    path('api/suggestions',views.suggestions,name='suggestions'),
]   
