from django import forms
from .models import Device
from customers.models import Customer


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['customer', 'device_type', 'brand', 'model', 'serial_number', 'problem', 'condition']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'device_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dell, HP, Lenovo'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Latitude 7480'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional serial number'}),
            'problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the problem reported by the customer'}),
            'condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Used, Minor scratches'}),
        }
