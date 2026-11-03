from django.db import models


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Utilities', 'Utilities (Electricity, Water)'),
        ('Equipment', 'Equipment & Tools'),
        ('Parts', 'Spare Parts Purchase'),
        ('Salaries', 'Salaries'),
        ('Marketing', 'Marketing & Advertising'),
        ('Software', 'Software & Subscriptions'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} — ${self.amount} ({self.date})"
