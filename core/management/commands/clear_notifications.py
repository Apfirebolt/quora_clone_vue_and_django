from django.core.management.base import BaseCommand
from core.models import Notification


class Command(BaseCommand):
    help = "Clears all notifications from the database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **options):
        notification_count = Notification.objects.count()
        
        if notification_count == 0:
            self.stdout.write(self.style.WARNING("No notifications found."))
            return

        if not options['confirm']:
            confirm = input(f"Are you sure you want to delete {notification_count} notifications? (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        deleted_count, _ = Notification.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted {deleted_count} notifications.")
        )
