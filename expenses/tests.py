from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense


class ExpenseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testadmin', password='password123', is_staff=True)
        self.client = Client()
        self.client.login(username='testadmin', password='password123')
        self.expense = Expense.objects.create(
            title='Shop Electricity',
            amount=Decimal('45.00'),
            category='Utilities',
            date='2026-10-01',
            notes='Monthly utility bill'
        )

    def test_expense_creation(self):
        """Expense record creation works with category and amount"""
        self.assertEqual(self.expense.title, 'Shop Electricity')
        self.assertEqual(self.expense.amount, Decimal('45.00'))
        self.assertEqual(self.expense.category, 'Utilities')
        self.assertIn('Shop Electricity', str(self.expense))

    def test_expense_list_view(self):
        """Expense list view loads and displays total expenses and net profit"""
        response = self.client.get(reverse('expenses:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shop Electricity')
        self.assertContains(response, '$45')

    def test_expense_search_and_filter(self):
        """Search and filter expenses by category"""
        response = self.client.get(reverse('expenses:expense_list') + '?category=Utilities')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shop Electricity')

        response = self.client.get(reverse('expenses:expense_list') + '?category=Rent')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Shop Electricity')
