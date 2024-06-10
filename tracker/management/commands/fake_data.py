# tracker/management/commands/generate_sample_data.py
import random
from django.core.management.base import BaseCommand
from faker import Faker
from tracker.models import tractor_brand, tractor_model, tractor_details, implements, customer
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Generate sample data for the asset tracking system'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create sample users
        for _ in range(15):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            user.save()

        # Create sample customers
        for _ in range(10):
            customers = customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                address=fake.address()
            )

        # Create sample tractor brands
        brands = []
        for _ in range(10):
            brand = tractor_brand.objects.create(name=fake.company())
            brands.append(brand)

        # Create sample tractor models
        models = []
        for brand in brands:
            for _ in range(20):
                model = tractor_model.objects.create(
                    brand=brand,
                    name=fake.word()
                )
                models.append(model)

        # Create sample tractors
        for _ in range(20):
            tractor_details.objects.create(
                brand=random.choice(brands),
                model=random.choice(models),
                registration_number=fake.unique.license_plate(),
                chassis_number=fake.unique.ean13(),
                engine_number=fake.unique.ean8(),
                color=fake.color_name(),
                owner=customer.objects.order_by('?').first(),
                updated_by=User.objects.order_by('?').first()
            )

        # Create sample implements
        for _ in range(20):
            implements.objects.create(
                brand=fake.company(),
                chassis_number=fake.unique.ean13(),
                color=fake.color_name(),
                owner=customer.objects.order_by('?').first(),
                updated_by=User.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))
