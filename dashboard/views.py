from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from customers.models import Customer
from devices.models import Device
from repairs.models import Repair
from payments.models import Payment
from expenses.models import Expense


@login_required
def dashboard(request):
    total_customers = Customer.objects.count()
    total_devices = Device.objects.count()
    total_repairs = Repair.objects.count()
    pending_repairs = Repair.objects.filter(status='Pending').count()
    repairing_count = Repair.objects.filter(status='Repairing').count()
    completed_repairs = Repair.objects.filter(status='Completed').count()
    delivered_repairs = Repair.objects.filter(status='Delivered').count()

    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_revenue - total_expenses

    # If the user is a technician (not staff), show only their assigned repairs
    if not request.user.is_staff and hasattr(request.user, 'technician_profile'):
        tech = request.user.technician_profile
        recent_repairs = Repair.objects.select_related(
            'customer', 'device', 'technician'
        ).filter(technician=tech).order_by('-received_date')[:10]
        is_technician_view = True
    else:
        recent_repairs = Repair.objects.select_related(
            'customer', 'device', 'technician'
        ).order_by('-received_date')[:10]
        is_technician_view = False

    context = {
        'total_customers': total_customers,
        'total_devices': total_devices,
        'total_repairs': total_repairs,
        'pending_repairs': pending_repairs,
        'repairing_count': repairing_count,
        'completed_repairs': completed_repairs,
        'delivered_repairs': delivered_repairs,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'recent_repairs': recent_repairs,
        'is_technician_view': is_technician_view,
    }
    return render(request, 'dashboard/dashboard.html', context)
