from django import forms
from .models import Technician


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name', 'phone', 'specialization', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mohamed Hassan'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 63xxxxxxx'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
