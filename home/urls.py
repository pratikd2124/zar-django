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
    
    path('support-tickets',views.support_ticket,name='support_ticket'),
    path('edit-pages',views.edit_pages,name='edit_pages'),
    
    path('edit-brand/<int:id>',views.update_brand,name='edit_brand'),
    path('edit-service-provide/<int:id>',views.update_service,name='update_service'),
    path('edit-gallery/<int:id>',views.update_gallery,name='update_gallery'),
]   
