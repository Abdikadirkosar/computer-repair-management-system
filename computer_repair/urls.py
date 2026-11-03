from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from dashboard.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Password change
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html',
    ), name='password_change_done'),
    # Dashboard (root redirect)
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard_alt'),
    # App URLs
    path('customers/', include('customers.urls')),
    path('devices/', include('devices.urls')),
    path('repairs/', include('repairs.urls')),
    path('technicians/', include('technicians.urls')),
    path('payments/', include('payments.urls')),
    path('expenses/', include('expenses.urls')),
]
