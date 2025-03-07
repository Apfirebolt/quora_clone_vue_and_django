import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Generates a random user'


    def handle(self, *args, **kwargs):
        users = list(CustomUser.objects.all())
        if users:
            random_user = random.choice(users)
            print(random_user.username)
        else:
            print("No users found.")


        
