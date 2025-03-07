import random
from django.core.management.base import BaseCommand
from core.models import Question
from faker import Faker
from django.utils.text import slugify
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Generates fake questions'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of questions to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        # Get a random author
        selected_author = CustomUser.objects.first()

        for _ in range(total):
            content = fake.sentence(nb_words=6)
            description = fake.paragraph(nb_sentences=3)
            slug = slugify(content)
            author = selected_author
            
            Question.objects.create(
                content=content,
                description=description,
                slug=slug,
                author=author
            )
