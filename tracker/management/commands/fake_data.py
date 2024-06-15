# tracker/management/commands/populate_fake_data.py

from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from tracker.models import Customer, TractorBrand, TractorModel, TractorDetails, Implement, OwnershipHistory
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Populate database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data
        Customer.objects.all().delete()
        TractorBrand.objects.all().delete()
        TractorModel.objects.all().delete()
        TractorDetails.objects.all().delete()
        Implement.objects.all().delete()
        OwnershipHistory.objects.all().delete()

        # Create Tractor Brands
        tractor_brands = []
        for _ in range(5):
            tractor_brands.append(TractorBrand.objects.create(name=fake.company()))

        # Create Tractor Models
        tractor_models = []
        for brand in tractor_brands:
            for _ in range(10):
                tractor_models.append(TractorModel.objects.create(brand=brand, name=fake.word()))

        # Create Customers
        customers = []
        for _ in range(20):
            customers.append(Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                created_at=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
            ))

        # Create Tractor Details
        tractor_details = []
        for _ in range(20):
            tractor_details.append(TractorDetails.objects.create(
                brand=random.choice(tractor_brands),
                model=random.choice(tractor_models),
                registration_number=fake.unique.uuid4(),
                chassis_number=fake.unique.uuid4(),
                engine_number=fake.unique.uuid4(),
                color=fake.color_name(),
                owner=random.choice(customers),
                updated_by=User.objects.first()  # Replace with actual user selection logic
            ))

        # Create Implements
        implements = []
        for _ in range(20):
            implements.append(Implement.objects.create(
                brand=fake.company(),
                chassis_number=fake.unique.uuid4(),
                color=fake.color_name(),
                owner=random.choice(customers),
                updated_by=User.objects.first()  # Replace with actual user selection logic
            ))

        # Create Ownership History
        ownership_history = []
        for tractor_detail in tractor_details:
            ownership_history.append(OwnershipHistory.objects.create(
                tractor=tractor_detail,
                previous_owner=random.choice(customers),
                new_owner=random.choice(customers),
                change_date=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone()),
                updated_by=User.objects.first()  # Replace with actual user selection logic
            ))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with fake data'))
