from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )
    else:
        customers = Customer.objects.all()

    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'query': query,
    })


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    devices = customer.devices.all()
    repairs = customer.repairs.select_related('device', 'technician').all()
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'devices': devices,
        'repairs': repairs,
    })


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f"Customer '{customer.name}' added successfully!")
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Add New Customer',
        'button_text': 'Save Customer',
    })


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer '{customer.name}' updated successfully!")
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'customer': customer,
        'title': f'Edit Customer: {customer.name}',
        'button_text': 'Update Customer',
    })


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f"Customer '{name}' deleted successfully.")
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {
        'customer': customer,
    })
