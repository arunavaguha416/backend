from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = get_random_string(12)  # Generate a random password

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f"Superuser created: username={username}, email={email}, password={password}"
            ))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))