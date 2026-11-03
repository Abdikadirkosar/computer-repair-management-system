from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Device
from .forms import DeviceForm


@login_required
def device_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        devices = Device.objects.filter(
            Q(brand__icontains=query) | Q(model__icontains=query) | Q(serial_number__icontains=query)
        ).select_related('customer')
    else:
        devices = Device.objects.select_related('customer').all()

    return render(request, 'devices/device_list.html', {
        'devices': devices,
        'query': query,
    })


@login_required
def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    repairs = device.repairs.select_related('technician').all()
    return render(request, 'devices/device_detail.html', {
        'device': device,
        'repairs': repairs,
    })


@login_required
def device_create(request):
    initial = {}
    customer_pk = request.GET.get('customer')
    if customer_pk:
        initial['customer'] = customer_pk
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save()
            messages.success(request, f"Device '{device}' added successfully!")
            return redirect('devices:device_detail', pk=device.pk)
    else:
        form = DeviceForm(initial=initial)
    return render(request, 'devices/device_form.html', {
        'form': form,
        'title': 'Add New Device',
        'button_text': 'Save Device',
    })


@login_required
def device_update(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, f"Device '{device}' updated successfully!")
            return redirect('devices:device_detail', pk=device.pk)
    else:
        form = DeviceForm(instance=device)
    return render(request, 'devices/device_form.html', {
        'form': form,
        'device': device,
        'title': f'Edit Device: {device}',
        'button_text': 'Update Device',
    })


@login_required
def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        name = str(device)
        customer_pk = device.customer_id
        device.delete()
        messages.success(request, f"Device '{name}' deleted successfully.")
        return redirect('customers:customer_detail', pk=customer_pk)
    return render(request, 'devices/device_confirm_delete.html', {
        'device': device,
    })
