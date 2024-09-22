# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('users',views.all_users,name='users_list'),
    path('community',views.all_community,name='all_community'),

    path('brand',views.all_brand,name='brand_list'),
    path('category',views.all_category,name='category_list'),
    
    path('send_passcode',views.send_passcode,name='send_passcode'),
    
    path('support-tickets',views.all_users,name='support_ticket'),
    path('edit-pages',views.edit_pages,name='edit_pages'),
    
]   
