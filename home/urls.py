# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('users',views.all_users,name='users_list'),
    path('community',views.all_community,name='all_community'),

    path('brand',views.all_brand,name='brand_list'),
    path('category',views.all_category,name='category_list'),
    
    
    path('support-tickets',views.all_users,name='support_ticket'),
]   
