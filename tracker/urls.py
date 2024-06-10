from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/new/', views.customer_create, name='customer_create'),
    path('tractors/', views.tractor_list, name='tractor_list'),
    path('tractors/new/', views.tractor_create, name='tractor_create'),
    path('implements/', views.implement_list, name='implement_list'),
    path('implements/new/', views.implement_create, name='implement_create'),
    path('tractors/<int:pk>/edit/', views.tractor_update, name='tractor_update'),
]
