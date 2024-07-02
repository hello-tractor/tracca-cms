from django.urls import path
from .views import create_device, success

urlpatterns = [
    path('create_device/', create_device, name='create_device'),
    path('success/', success, name='success'),
    # Add other URL patterns here
]
