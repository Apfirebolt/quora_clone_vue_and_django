import random
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from faker import Faker

class Command(BaseCommand):
    help = 'Generates fake users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        for _ in range(total):
            CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
        self.stdout.write(self.style.SUCCESS(f'{total} users created successfully!'))