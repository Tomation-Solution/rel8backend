from django.urls import path

from . import views

urlpatterns = [
    path('technical/',views.TechnicalSuppportView.as_view(), name='technical_support'),
    path('admin/',views.AdminSuppportView.as_view(), name='admin_support'),
]