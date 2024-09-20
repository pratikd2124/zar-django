# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home-owner/', views.home_owner_view, name='home_owner'),
    path('service-provider/', views.submit_service_provider, name='submit_service_provider'),
    path('material-provider/', views.submit_material_provider, name='submit_material_provider'),
    path('success/', views.success_page, name='success_page'),
    path('',views.home,name='home'),
    path('validate',views.validate,name='validate')
]   
