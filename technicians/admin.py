from django.contrib import admin
from .models import Technician


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'specialization', 'status', 'created_at')
    search_fields = ('name', 'phone')
    list_filter = ('specialization', 'status')
    ordering = ('name',)
