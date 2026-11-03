from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Technician
from .forms import TechnicianForm


@login_required
def technician_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        technicians = Technician.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )
    else:
        technicians = Technician.objects.all()

    return render(request, 'technicians/technician_list.html', {
        'technicians': technicians,
        'query': query,
    })


@login_required
def technician_detail(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    repairs = technician.repairs.select_related('customer', 'device').all()
    return render(request, 'technicians/technician_detail.html', {
        'technician': technician,
        'repairs': repairs,
    })


@login_required
def technician_create(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            technician = form.save()
            messages.success(request, f"Technician '{technician.name}' added successfully!")
            return redirect('technicians:technician_detail', pk=technician.pk)
    else:
        form = TechnicianForm()
    return render(request, 'technicians/technician_form.html', {
        'form': form,
        'title': 'Add New Technician',
        'button_text': 'Save Technician',
    })


@login_required
def technician_update(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        form = TechnicianForm(request.POST, instance=technician)
        if form.is_valid():
            form.save()
            messages.success(request, f"Technician '{technician.name}' updated successfully!")
            return redirect('technicians:technician_detail', pk=technician.pk)
    else:
        form = TechnicianForm(instance=technician)
    return render(request, 'technicians/technician_form.html', {
        'form': form,
        'technician': technician,
        'title': f'Edit Technician: {technician.name}',
        'button_text': 'Update Technician',
    })


@login_required
def technician_delete(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        name = technician.name
        technician.delete()
        messages.success(request, f"Technician '{name}' deleted successfully.")
        return redirect('technicians:technician_list')
    return render(request, 'technicians/technician_confirm_delete.html', {
        'technician': technician,
    })
