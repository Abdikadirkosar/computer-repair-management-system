from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('record/', views.payment_create_general, name='payment_create_general'),
    path('repair/<int:repair_pk>/add/', views.payment_create, name='payment_create'),
    path('<int:pk>/delete/', views.payment_delete, name='payment_delete'),
]
