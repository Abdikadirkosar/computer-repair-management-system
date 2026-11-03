from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer


class CustomerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testadmin', password='password123')
        self.client = Client()
        self.client.login(username='testadmin', password='password123')
        self.customer = Customer.objects.create(
            name='Ahmed Ali',
            phone='634441111',
            email='ahmed@example.com',
            address='Hargeisa'
        )

    def test_customer_creation(self):
        """Customer creation works"""
        self.assertEqual(self.customer.name, 'Ahmed Ali')
        self.assertEqual(self.customer.phone, '634441111')
        self.assertEqual(str(self.customer), 'Ahmed Ali (634441111)')

    def test_customer_list_works(self):
        """Customer list view loads and displays customer"""
        response = self.client.get(reverse('customers:customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ahmed Ali')
        self.assertContains(response, '634441111')

    def test_customer_search_works(self):
        """Search customer by name or phone"""
        response = self.client.get(reverse('customers:customer_list') + '?q=Ahmed')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ahmed Ali')

        response = self.client.get(reverse('customers:customer_list') + '?q=999999999')
        self.assertNotContains(response, 'Ahmed Ali')
