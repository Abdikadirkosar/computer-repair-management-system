from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Repair
from .forms import RepairForm, RepairUpdateForm, RepairQuickStatusForm


@login_required
def repair_list(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    repairs = Repair.objects.select_related('customer', 'device', 'technician').all()

    # If logged-in user is a technician (not staff), they can filter to my repairs
    my_repairs_only = request.GET.get('my_repairs') == '1'
    if my_repairs_only or (hasattr(request.user, 'technician_profile') and not request.user.is_staff):
        if hasattr(request.user, 'technician_profile'):
            repairs = repairs.filter(technician=request.user.technician_profile)

    if query:
        repairs = repairs.filter(
            Q(repair_number__icontains=query) |
            Q(customer__name__icontains=query) |
            Q(customer__phone__icontains=query) |
            Q(device__brand__icontains=query) |
            Q(device__model__icontains=query)
        )

    if status_filter:
        repairs = repairs.filter(status=status_filter)

    status_choices = Repair.STATUS_CHOICES
    return render(request, 'repairs/repair_list.html', {
        'repairs': repairs,
        'query': query,
        'status_filter': status_filter,
        'status_choices': status_choices,
        'my_repairs_only': my_repairs_only,
    })


@login_required
def repair_detail(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    payments = repair.payments.all()
    status_form = RepairQuickStatusForm(instance=repair)
    return render(request, 'repairs/repair_detail.html', {
        'repair': repair,
        'payments': payments,
        'status_form': status_form,
    })


@login_required
def repair_quick_update(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    if request.method == 'POST':
        form = RepairQuickStatusForm(request.POST, instance=repair)
        if form.is_valid():
            form.save()
            messages.success(request, f"Repair '{repair.repair_number}' status updated to '{repair.status}'!")
        else:
            messages.error(request, "Failed to update repair status. Please check your inputs.")
    return redirect('repairs:repair_detail', pk=repair.pk)


@login_required
def repair_create(request):
    initial = {}
    customer_pk = request.GET.get('customer')
    device_pk = request.GET.get('device')
    if customer_pk:
        initial['customer'] = customer_pk
    if device_pk:
        initial['device'] = device_pk

    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair = form.save()
            messages.success(request, f"Repair '{repair.repair_number}' created successfully!")
            return redirect('repairs:repair_detail', pk=repair.pk)
    else:
        form = RepairForm(initial=initial)
    return render(request, 'repairs/repair_form.html', {
        'form': form,
        'title': 'Create New Repair',
        'button_text': 'Create Repair',
    })


@login_required
def repair_update(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repair)
        if form.is_valid():
            form.save()
            messages.success(request, f"Repair '{repair.repair_number}' updated successfully!")
            return redirect('repairs:repair_detail', pk=repair.pk)
    else:
        form = RepairForm(instance=repair)
    return render(request, 'repairs/repair_form.html', {
        'form': form,
        'repair': repair,
        'title': f'Edit Repair: {repair.repair_number}',
        'button_text': 'Update Repair',
    })


@login_required
def repair_delete(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    if request.method == 'POST':
        repair_num = repair.repair_number
        repair.delete()
        messages.success(request, f"Repair '{repair_num}' deleted successfully.")
        return redirect('repairs:repair_list')
    return render(request, 'repairs/repair_confirm_delete.html', {
        'repair': repair,
    })


@login_required
def repair_receipt(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    payments = repair.payments.all()
    return render(request, 'repairs/repair_receipt.html', {
        'repair': repair,
        'payments': payments,
    })


@login_required
def get_customer_devices(request):
    """AJAX endpoint to get devices belonging to a specific customer."""
    customer_id = request.GET.get('customer_id')
    from devices.models import Device
    from django.http import JsonResponse

    if customer_id:
        devices = Device.objects.filter(customer_id=customer_id).values('id', 'brand', 'model', 'device_type')
        return JsonResponse({'devices': list(devices)})
    return JsonResponse({'devices': []})
