from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        email = 'test@example.com'
        password = 'admin@1234'  # Set fixed password

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f"Superuser created: email={email}, password={password}"
            ))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))