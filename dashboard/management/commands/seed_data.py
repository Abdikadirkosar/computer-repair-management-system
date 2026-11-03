from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from customers.models import Customer
from devices.models import Device
from technicians.models import Technician
from repairs.models import Repair
from payments.models import Payment


class Command(BaseCommand):
    help = 'Seeds the database with sample data for demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding sample data for Computer Repair Management System...")

        # 1. Create Users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@repairshop.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        tech_user, created = User.objects.get_or_create(
            username='tech',
            defaults={
                'email': 'tech@repairshop.com',
                'is_staff': False,
            }
        )
        if created:
            tech_user.set_password('tech123')
            tech_user.save()
            self.stdout.write(self.style.SUCCESS("Created technician user: tech / tech123"))

        # 2. Create Technicians
        tech1, _ = Technician.objects.get_or_create(
            name='Mohamed Hassan',
            defaults={
                'user': tech_user,
                'phone': '634449911',
                'specialization': 'Laptop Repair',
                'status': 'Active'
            }
        )
        tech2, _ = Technician.objects.get_or_create(
            name='Abdi Omar',
            defaults={
                'phone': '634449922',
                'specialization': 'Desktop Repair',
                'status': 'Active'
            }
        )
        self.stdout.write(self.style.SUCCESS("Created Technicians: Mohamed Hassan, Abdi Omar"))

        # 3. Create Customers
        cust1, _ = Customer.objects.get_or_create(
            name='Ahmed Ali',
            defaults={
                'phone': '634441111',
                'email': 'ahmed.ali@example.com',
                'address': 'Jigjiga Yar, Hargeisa'
            }
        )
        cust2, _ = Customer.objects.get_or_create(
            name='Mohamed Hassan',
            defaults={
                'phone': '634442222',
                'email': 'mohamed.h@example.com',
                'address': '26 June, Hargeisa'
            }
        )
        cust3, _ = Customer.objects.get_or_create(
            name='Abdi Yusuf',
            defaults={
                'phone': '634443333',
                'email': 'abdi.y@example.com',
                'address': 'Ibrahim Koodbuur, Hargeisa'
            }
        )
        self.stdout.write(self.style.SUCCESS("Created Customers: Ahmed Ali, Mohamed Hassan, Abdi Yusuf"))

        # 4. Create Devices
        dev1, _ = Device.objects.get_or_create(
            customer=cust1,
            brand='Dell',
            model='Latitude 7480',
            defaults={
                'device_type': 'Laptop',
                'serial_number': 'DL7480-001',
                'problem': 'Laptop does not turn on',
                'condition': 'Used'
            }
        )
        dev2, _ = Device.objects.get_or_create(
            customer=cust2,
            brand='HP',
            model='ProBook 450 G7',
            defaults={
                'device_type': 'Laptop',
                'serial_number': 'HP450-998',
                'problem': 'Screen flickering and broken hinge',
                'condition': 'Minor scratches'
            }
        )
        dev3, _ = Device.objects.get_or_create(
            customer=cust3,
            brand='Lenovo',
            model='ThinkPad T480',
            defaults={
                'device_type': 'Laptop',
                'serial_number': 'TP-E14-772',
                'problem': 'Battery not charging and slow boot',
                'condition': 'Good'
            }
        )
        dev4, _ = Device.objects.get_or_create(
            customer=cust1,
            brand='Epson',
            model='EcoTank L3150',
            defaults={
                'device_type': 'Printer',
                'serial_number': 'EP-L3150-12',
                'problem': 'Paper jam and ink cartridge error',
                'condition': 'Used'
            }
        )
        self.stdout.write(self.style.SUCCESS("Created Devices: Dell Latitude 7480, HP ProBook, Lenovo ThinkPad, Epson Printer"))

        # 5. Create Repairs & Payments
        # Repair 1: Completed, fully paid ($40)
        rep1, created1 = Repair.objects.get_or_create(
            repair_number='REP-0001',
            defaults={
                'customer': cust1,
                'device': dev1,
                'technician': tech1,
                'priority': 'Normal',
                'problem': 'Laptop does not turn on',
                'diagnosis': 'Power circuit problem with shorted capacitor',
                'repair_notes': 'Replaced power capacitor and cleaned motherboard.',
                'status': 'Completed',
                'cost': Decimal('40.00'),
                'received_date': timezone.now().date(),
                'completed_date': timezone.now().date(),
            }
        )
        if created1:
            Payment.objects.create(
                repair=rep1,
                amount=Decimal('40.00'),
                payment_method='Cash',
                payment_date=timezone.now().date()
            )

        # Repair 2: Repairing, partially paid ($30 paid of $65)
        rep2, created2 = Repair.objects.get_or_create(
            repair_number='REP-0002',
            defaults={
                'customer': cust2,
                'device': dev2,
                'technician': tech1,
                'priority': 'Urgent',
                'problem': 'Screen flickering and broken hinge',
                'diagnosis': 'Damaged display LVDS cable and cracked right hinge',
                'repair_notes': 'Display cable replaced. Waiting for replacement hinge bracket.',
                'status': 'Repairing',
                'cost': Decimal('65.00'),
                'received_date': timezone.now().date(),
            }
        )
        if created2:
            Payment.objects.create(
                repair=rep2,
                amount=Decimal('30.00'),
                payment_method='ZAAD',
                payment_date=timezone.now().date()
            )

        # Repair 3: Pending, no payment yet ($50 cost)
        Repair.objects.get_or_create(
            repair_number='REP-0003',
            defaults={
                'customer': cust3,
                'device': dev3,
                'technician': tech2,
                'priority': 'Normal',
                'problem': 'Battery not charging and slow boot',
                'diagnosis': 'Preliminary check: battery health degraded below 20%',
                'repair_notes': 'Customer advised to replace battery pack.',
                'status': 'Pending',
                'cost': Decimal('50.00'),
                'received_date': timezone.now().date(),
            }
        )

        # Repair 4: Delivered, fully paid ($25)
        rep4, created4 = Repair.objects.get_or_create(
            repair_number='REP-0004',
            defaults={
                'customer': cust1,
                'device': dev4,
                'technician': tech2,
                'priority': 'Normal',
                'problem': 'Paper jam and ink cartridge error',
                'diagnosis': 'Foreign object inside paper roller feeder',
                'repair_notes': 'Removed jammed paper, cleaned feed rollers, aligned print head.',
                'status': 'Delivered',
                'cost': Decimal('25.00'),
                'received_date': timezone.now().date(),
                'completed_date': timezone.now().date(),
            }
        )
        # 6. Create Sample Expenses
        from expenses.models import Expense
        Expense.objects.get_or_create(
            title='Shop Electricity & Internet',
            defaults={
                'amount': Decimal('35.00'),
                'category': 'Utilities',
                'date': timezone.now().date(),
                'notes': 'Monthly utilities payment'
            }
        )
        Expense.objects.get_or_create(
            title='Thermal Paste & Screwdriver Kit',
            defaults={
                'amount': Decimal('18.00'),
                'category': 'Equipment',
                'date': timezone.now().date(),
                'notes': 'Tools replacement for workshop'
            }
        )
        Expense.objects.get_or_create(
            title='Laptop Screen & Ribbon Cables Stock',
            defaults={
                'amount': Decimal('32.00'),
                'category': 'Parts',
                'date': timezone.now().date(),
                'notes': 'Replacement parts inventory batch'
            }
        )
        self.stdout.write(self.style.SUCCESS("Created sample Expenses: Utilities, Equipment, Parts"))

        self.stdout.write(self.style.SUCCESS("Sample data seeding complete!"))
