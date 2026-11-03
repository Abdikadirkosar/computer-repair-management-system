from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=150, help_text="Full name of customer")
    phone = models.CharField(max_length=30, help_text="Phone number")
    email = models.EmailField(blank=True, null=True, help_text="Optional email address")
    address = models.TextField(blank=True, null=True, help_text="Optional address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"
