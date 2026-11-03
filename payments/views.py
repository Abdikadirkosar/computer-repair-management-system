from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Payment
from .forms import PaymentForm, GeneralPaymentForm
from repairs.models import Repair


@login_required
def payment_list(request):
    query = request.GET.get('q', '').strip()
    payments = Payment.objects.select_related('repair', 'repair__customer', 'repair__device').all()

    if query:
        payments = payments.filter(
            Q(repair__repair_number__icontains=query) |
            Q(repair__customer__name__icontains=query) |
            Q(payment_method__icontains=query)
        )

    return render(request, 'payments/payment_list.html', {
        'payments': payments,
        'query': query,
    })


@login_required
def payment_create(request, repair_pk):
    repair = get_object_or_404(Repair, pk=repair_pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.repair = repair
            try:
                payment.full_clean()
                payment.save()
                messages.success(request, f"Payment of ${payment.amount:.2f} recorded successfully!")
                return redirect('repairs:repair_detail', pk=repair.pk)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {
        'form': form,
        'repair': repair,
    })


@login_required
def payment_create_general(request):
    """Create a payment by choosing from any repair."""
    if request.method == 'POST':
        form = GeneralPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            try:
                payment.full_clean()
                payment.save()
                messages.success(request, f"Payment of ${payment.amount:.2f} recorded for {payment.repair.repair_number}!")
                return redirect('payments:payment_list')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
    else:
        form = GeneralPaymentForm()

    return render(request, 'payments/payment_general_form.html', {
        'form': form,
    })


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if not request.user.is_staff:
        messages.error(request, "Only admins can delete payment records.")
        return redirect('repairs:repair_detail', pk=payment.repair_id)

    if request.method == 'POST':
        repair_pk = payment.repair_id
        amount = payment.amount
        payment.delete()
        messages.success(request, f"Payment of ${amount:.2f} deleted successfully.")
        return redirect('repairs:repair_detail', pk=repair_pk)

    return render(request, 'payments/payment_confirm_delete.html', {
        'payment': payment,
    })
