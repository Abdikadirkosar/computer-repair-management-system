from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Expense
from .forms import ExpenseForm
from payments.models import Payment


@login_required
def expense_list(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()

    expenses = Expense.objects.all()

    if query:
        expenses = expenses.filter(
            Q(title__icontains=query) | Q(notes__icontains=query)
        )
    if category_filter:
        expenses = expenses.filter(category=category_filter)

    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_revenue - total_expenses

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'query': query,
        'category_filter': category_filter,
        'category_choices': Expense.CATEGORY_CHOICES,
        'total_expenses': total_expenses,
        'total_revenue': total_revenue,
        'net_profit': net_profit,
    })


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            messages.success(request, f"Expense '{expense.title}' recorded successfully!")
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'title': 'Record New Expense',
        'button_text': 'Save Expense',
    })


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, f"Expense '{expense.title}' updated successfully!")
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'expense': expense,
        'title': f'Edit Expense: {expense.title}',
        'button_text': 'Update Expense',
    })


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        title = expense.title
        expense.delete()
        messages.success(request, f"Expense '{title}' deleted successfully.")
        return redirect('expenses:expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {
        'expense': expense,
    })
