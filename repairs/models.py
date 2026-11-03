from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from customers.models import Customer
from devices.models import Device
from technicians.models import Technician


class Repair(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Repairing', 'Repairing'),
        ('Completed', 'Completed'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
    ]

    repair_number = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='repairs')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='repairs')
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True, related_name='repairs')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    problem = models.TextField(help_text="Reported problem description")
    diagnosis = models.TextField(blank=True, help_text="Technician diagnosis findings")
    repair_notes = models.TextField(blank=True, help_text="Notes on parts replaced or repair progress")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="Total estimated or final repair cost")
    received_date = models.DateField(default=timezone.now)
    completed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.cost is not None and self.cost < Decimal('0.00'):
            raise ValidationError({'cost': 'Repair cost cannot be negative.'})

    def save(self, *args, **kwargs):
        if not self.repair_number:
            last_repair = Repair.objects.all().order_by('id').last()
            if last_repair and last_repair.repair_number and last_repair.repair_number.startswith('REP-'):
                try:
                    num = int(last_repair.repair_number.split('-')[1]) + 1
                except (IndexError, ValueError):
                    num = Repair.objects.count() + 1
            else:
                num = Repair.objects.count() + 1
            self.repair_number = f"REP-{num:04d}"

        if self.status in ['Completed', 'Delivered'] and not self.completed_date:
            self.completed_date = timezone.now().date()
        super().save(*args, **kwargs)

    @property
    def total_paid(self):
        total = self.payments.aggregate(models.Sum('amount'))['amount__sum']
        return total or Decimal('0.00')

    @property
    def balance(self):
        remaining = self.cost - self.total_paid
        return remaining if remaining > Decimal('0.00') else Decimal('0.00')

    @property
    def is_fully_paid(self):
        return self.cost > Decimal('0.00') and self.balance <= Decimal('0.00')

    def __str__(self):
        return f"{self.repair_number} - {self.device} ({self.status})"
