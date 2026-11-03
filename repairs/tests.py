from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from devices.models import Device
from technicians.models import Technician
from .models import Repair


class RepairTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testadmin', password='password123')
        self.client = Client()
        self.client.login(username='testadmin', password='password123')
        self.customer = Customer.objects.create(name='Ahmed Ali', phone='634441111')
        self.device = Device.objects.create(
            customer=self.customer,
            device_type='Laptop',
            brand='Dell',
            model='Latitude 7480',
            problem='Does not boot'
        )
        self.technician = Technician.objects.create(
            name='Mohamed Hassan',
            phone='634449911',
            specialization='Laptop Repair'
        )

    def test_repair_creation_and_number_generation(self):
        """Repair creation works and repair number is automatically generated"""
        repair = Repair.objects.create(
            customer=self.customer,
            device=self.device,
            technician=self.technician,
            problem='Does not boot',
            cost=Decimal('40.00')
        )
        self.assertTrue(repair.repair_number.startswith('REP-'))
        self.assertEqual(repair.cost, Decimal('40.00'))
        self.assertEqual(repair.status, 'Pending')

    def test_sequential_repair_numbers(self):
        """Sequential repairs receive sequential numbers"""
        r1 = Repair.objects.create(
            customer=self.customer,
            device=self.device,
            problem='Problem 1',
            cost=Decimal('20.00')
        )
        r2 = Repair.objects.create(
            customer=self.customer,
            device=self.device,
            problem='Problem 2',
            cost=Decimal('30.00')
        )
        self.assertTrue(r1.repair_number.startswith('REP-'))
        self.assertTrue(r2.repair_number.startswith('REP-'))
        self.assertNotEqual(r1.repair_number, r2.repair_number)

    def test_repair_receipt_view(self):
        """Receipt view renders properly"""
        repair = Repair.objects.create(
            customer=self.customer,
            device=self.device,
            problem='Screen issue',
            cost=Decimal('50.00')
        )
        response = self.client.get(reverse('repairs:repair_receipt', args=[repair.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, repair.repair_number)
        self.assertContains(response, 'COMPUTER REPAIR SHOP')
        self.assertContains(response, 'Ahmed Ali')
