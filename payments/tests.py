from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from customers.models import Customer
from devices.models import Device
from repairs.models import Repair
from .models import Payment


class PaymentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testadmin', password='password123', is_staff=True)
        self.client = Client()
        self.client.login(username='testadmin', password='password123')
        self.customer = Customer.objects.create(name='Ahmed Ali', phone='634441111')
        self.device = Device.objects.create(
            customer=self.customer,
            device_type='Laptop',
            brand='Dell',
            model='Latitude 7480',
            problem='Power issue'
        )
        self.repair = Repair.objects.create(
            customer=self.customer,
            device=self.device,
            problem='Power issue',
            cost=Decimal('50.00')
        )

    def test_payment_creation_and_balance_calculation(self):
        """Payment is created and balance is calculated correctly"""
        self.assertEqual(self.repair.total_paid, Decimal('0.00'))
        self.assertEqual(self.repair.balance, Decimal('50.00'))

        # Pay $30
        p1 = Payment.objects.create(
            repair=self.repair,
            amount=Decimal('30.00'),
            payment_method='Cash'
        )
        self.assertEqual(self.repair.total_paid, Decimal('30.00'))
        self.assertEqual(self.repair.balance, Decimal('20.00'))

        # Pay another $20
        p2 = Payment.objects.create(
            repair=self.repair,
            amount=Decimal('20.00'),
            payment_method='ZAAD'
        )
        self.assertEqual(self.repair.total_paid, Decimal('50.00'))
        self.assertEqual(self.repair.balance, Decimal('0.00'))
        self.assertTrue(self.repair.is_fully_paid)

    def test_payment_cannot_exceed_balance(self):
        """Payment cannot exceed remaining balance"""
        # Attempt to pay $60 when cost is $50
        over_payment = Payment(
            repair=self.repair,
            amount=Decimal('60.00'),
            payment_method='Cash'
        )
        with self.assertRaises(ValidationError):
            over_payment.full_clean()

    def test_payment_must_be_greater_than_zero(self):
        """Payment amount must be strictly greater than 0"""
        zero_payment = Payment(
            repair=self.repair,
            amount=Decimal('0.00'),
            payment_method='Cash'
        )
        with self.assertRaises(ValidationError):
            zero_payment.full_clean()

        negative_payment = Payment(
            repair=self.repair,
            amount=Decimal('-10.00'),
            payment_method='Cash'
        )
        with self.assertRaises(ValidationError):
            negative_payment.full_clean()
