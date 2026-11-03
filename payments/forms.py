from decimal import Decimal
from django import forms
from .models import Payment
from repairs.models import Repair


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'payment_date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '0.00'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= Decimal('0.00'):
            raise forms.ValidationError("Payment amount must be greater than 0.")
        return amount


class GeneralPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['repair', 'amount', 'payment_method', 'payment_date']
        widgets = {
            'repair': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '0.00'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['repair'].queryset = Repair.objects.select_related('customer', 'device').all()

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= Decimal('0.00'):
            raise forms.ValidationError("Payment amount must be greater than 0.")
        return amount
