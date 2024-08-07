
from django.contrib import admin
from django.urls import path
from . import views
from .views import create_device, success, add_new_device
from live_tracking_data.admin import admin_site

urlpatterns = [
    path('create_device/', create_device, name='create_device'),
    path('add_new_device/', views.add_new_device, name='add_new_device'),
    path('success/', success, name='success'),
    path('admin/', admin_site.urls),
    # Add other URL patterns here
]
