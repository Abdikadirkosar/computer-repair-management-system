from django import forms
from .models import Repair
from customers.models import Customer
from devices.models import Device
from technicians.models import Technician


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = [
            'customer', 'device', 'technician', 'priority',
            'problem', 'diagnosis', 'repair_notes',
            'status', 'cost', 'received_date', 'completed_date'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'id': 'id_customer'}),
            'device': forms.Select(attrs={'class': 'form-control', 'id': 'id_device'}),
            'technician': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the problem reported'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Technician diagnosis (can be filled later)'}),
            'repair_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Repair notes, parts replaced, etc.'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['device'].queryset = Device.objects.filter(customer_id=customer_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.customer:
            self.fields['device'].queryset = self.instance.customer.devices.all()
        elif self.initial.get('customer'):
            self.fields['device'].queryset = Device.objects.filter(customer_id=self.initial['customer'])

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost is not None and cost < 0:
            raise forms.ValidationError("Repair cost cannot be negative.")
        return cost

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        device = cleaned_data.get('device')

        if not customer:
            self.add_error('customer', "Repair must have a customer.")
        if not device:
            self.add_error('device', "Repair must have a device.")

        if customer and device:
            if device.customer != customer:
                self.add_error('device', "Selected device does not belong to the selected customer.")
        return cleaned_data


class RepairUpdateForm(forms.ModelForm):
    """Simplified form for technicians to update repair status/diagnosis/notes."""
    class Meta:
        model = Repair
        fields = ['technician', 'diagnosis', 'repair_notes', 'status', 'cost', 'completed_date']
        widgets = {
            'technician': forms.Select(attrs={'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'repair_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class RepairQuickStatusForm(forms.ModelForm):
    """Quick 1-click status and diagnosis update for technicians directly on detail page."""
    class Meta:
        model = Repair
        fields = ['status', 'diagnosis', 'repair_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Technician diagnosis findings...'}),
            'repair_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Parts replaced, labor notes, etc.'}),
        }
