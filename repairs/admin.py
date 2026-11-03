from django.contrib import admin
from .models import Repair


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('repair_number', 'customer', 'device', 'technician', 'status', 'cost', 'created_at')
    search_fields = ('repair_number', 'customer__name', 'device__brand', 'device__model')
    list_filter = ('status', 'priority', 'created_at')
    readonly_fields = ('repair_number',)
    ordering = ('-created_at',)
