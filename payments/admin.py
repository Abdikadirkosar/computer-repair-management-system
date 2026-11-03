from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('repair', 'amount', 'payment_method', 'payment_date', 'created_at')
    search_fields = ('repair__repair_number', 'repair__customer__name')
    list_filter = ('payment_method', 'payment_date')
    ordering = ('-created_at',)
