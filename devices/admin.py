from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'device_type', 'customer', 'created_at')
    search_fields = ('brand', 'model', 'serial_number', 'customer__name')
    list_filter = ('device_type', 'created_at')
    ordering = ('-created_at',)
