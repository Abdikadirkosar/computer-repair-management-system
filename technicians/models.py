from django.db import models
from django.contrib.auth.models import User


class Technician(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Laptop Repair', 'Laptop Repair'),
        ('Desktop Repair', 'Desktop Repair'),
        ('Printer Repair', 'Printer Repair'),
        ('Software', 'Software'),
        ('General', 'General'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='technician_profile', help_text="Optional user account for login")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES, default='General')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.specialization})"
