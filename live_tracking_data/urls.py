from django.urls import path
from . import views
from .views import create_device, success, add_new_device

urlpatterns = [
    path('create_device/', create_device, name='create_device'),
    path('add_new_device/', views.add_new_device, name='add_new_device'),
    path('success/', success, name='success'),
    # Add other URL patterns here
]
