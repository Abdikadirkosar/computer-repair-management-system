from django.urls import path
from . import views

app_name = 'technicians'

urlpatterns = [
    path('', views.technician_list, name='technician_list'),
    path('create/', views.technician_create, name='technician_create'),
    path('<int:pk>/', views.technician_detail, name='technician_detail'),
    path('<int:pk>/edit/', views.technician_update, name='technician_update'),
    path('<int:pk>/delete/', views.technician_delete, name='technician_delete'),
]
