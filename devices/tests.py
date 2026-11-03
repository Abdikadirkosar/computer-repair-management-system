from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from .models import Device


class DeviceTests(TestCase):
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
            serial_number='DL7480-001',
            problem='Laptop does not turn on'
        )

    def test_device_belongs_to_customer(self):
        """Device belongs to customer"""
        self.assertEqual(self.device.customer, self.customer)
        self.assertIn(self.device, self.customer.devices.all())

    def test_device_list_works(self):
        """Device list view loads"""
        response = self.client.get(reverse('devices:device_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dell')
        self.assertContains(response, 'Latitude 7480')
