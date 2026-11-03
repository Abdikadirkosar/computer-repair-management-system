from django.urls import path
from . import views

app_name = 'repairs'

urlpatterns = [
    path('', views.repair_list, name='repair_list'),
    path('create/', views.repair_create, name='repair_create'),
    path('<int:pk>/', views.repair_detail, name='repair_detail'),
    path('<int:pk>/quick-update/', views.repair_quick_update, name='repair_quick_update'),
    path('<int:pk>/edit/', views.repair_update, name='repair_update'),
    path('<int:pk>/delete/', views.repair_delete, name='repair_delete'),
    path('<int:pk>/receipt/', views.repair_receipt, name='repair_receipt'),
    path('api/customer-devices/', views.get_customer_devices, name='customer_devices_api'),
]
