from django.db import models
from customers.models import Customer


class Device(models.Model):
    DEVICE_TYPE_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Printer', 'Printer'),
        ('Monitor', 'Monitor'),
        ('Other', 'Other'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='devices')
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES, default='Laptop')
    brand = models.CharField(max_length=100, help_text="e.g. Dell, HP, Lenovo")
    model = models.CharField(max_length=100, help_text="e.g. Latitude 7480, ThinkPad T480")
    serial_number = models.CharField(max_length=100, blank=True, help_text="Device serial number or identifier")
    problem = models.TextField(help_text="Customer reported problem")
    condition = models.CharField(max_length=100, blank=True, help_text="e.g. Used, Minor scratches, New")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.customer.name})"
