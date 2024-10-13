# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('users',views.all_users,name='users_list'),
    path('community',views.all_community,name='all_community'),

    path('brand',views.all_brand,name='brand_list'),
    path('service-provider',views.service_providers,name='service_provider'),
    path('category',views.all_category,name='category_list'),
    
    path('send_passcode',views.send_passcode,name='send_passcode'),
    
    path('support-tickets',views.support_ticket,name='support_ticket'),
    path('edit-pages',views.edit_pages,name='edit_pages'),
    
    path('terms/', views.terms_view, name='terms'),
    path('terms/delete/<str:model_name>/<int:section_id>/', views.delete_section, name='delete_section'),

    path('privacy-policy/', views.privacy_policy_view, name='manage_privacy_policy'),
    path('faq/', views.faq_view, name='manage_faq'),
    # path('delete/<str:model>/<int:section_id>/', views.delete_section, name='delete_section'),
    
    path('faq/delete/<int:id>/', views.delete_faq, name='delete_faq'),
    path('privacy/delete/<int:id>/', views.delete_privacy, name='delete_privacy'),
    
    path('edit-brand/<int:id>',views.update_brand,name='edit_brand'),
    path('edit-service-provide/<int:id>',views.update_service,name='update_service'),
    path('edit-gallery/<int:id>',views.update_gallery,name='update_gallery'),
    path('edit-user-info/<int:id>',views.update_user_info,name='update_user_info'),
    
    path('contact_page',views.contact_page,name='contact_page'),
    path('export',views.export,name='export'),
    
    
    path('analytics/<int:id>',views.detail_analytics,name='detail_analytics'),
    
    path('send-email/', views.send_custom_email, name='send_email'),
    path('email-list/', views.email_list, name='email_list'),
    path('view-email/', views.view_email, name='view_email'),
    

    
]   

