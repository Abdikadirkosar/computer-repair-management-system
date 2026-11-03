from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from repairs.models import Repair


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('ZAAD', 'ZAAD'),
        ('eDahab', 'eDahab'),
        ('Card', 'Card'),
        ('Bank', 'Bank'),
    ]

    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    payment_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.amount is not None:
            if self.amount <= Decimal('0.00'):
                raise ValidationError({'amount': 'Payment amount must be greater than 0.'})

            if self.repair_id:
                # Calculate currently paid amount excluding this payment instance if editing
                existing_payments = self.repair.payments.all()
                if self.pk:
                    existing_payments = existing_payments.exclude(pk=self.pk)
                already_paid = existing_payments.aggregate(models.Sum('amount'))['amount__sum'] or Decimal('0.00')
                remaining_balance = self.repair.cost - already_paid
                if remaining_balance < Decimal('0.00'):
                    remaining_balance = Decimal('0.00')

                if self.amount > remaining_balance:
                    raise ValidationError({
                        'amount': f"Payment amount (${self.amount:.2f}) cannot exceed the remaining balance (${remaining_balance:.2f})."
                    })

    def __str__(self):
        return f"Payment #{self.id} - {self.repair.repair_number} - ${self.amount}"
