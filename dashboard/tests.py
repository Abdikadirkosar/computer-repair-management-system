from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from devices.models import Device
from repairs.models import Repair
from payments.models import Payment


class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testadmin', password='password123')
        self.client = Client()
        self.client.login(username='testadmin', password='password123')

        cust = Customer.objects.create(name='Ahmed Ali', phone='634441111')
        dev = Device.objects.create(customer=cust, brand='Dell', model='7480', problem='Broken')
        rep = Repair.objects.create(customer=cust, device=dev, cost=Decimal('40.00'), status='Completed')
        Payment.objects.create(repair=rep, amount=Decimal('40.00'), payment_method='Cash')

    def test_dashboard_loads_successfully(self):
        """Dashboard loads with HTTP 200 and displays statistics"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total Customers')
        self.assertContains(response, 'Total Devices')
        self.assertContains(response, 'Total Repairs')
        self.assertContains(response, 'Total Revenue')
        self.assertContains(response, '$40')
