from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@admin.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "P@ssw0rd")

        if not User.objects.filter(email=email).exists():

            User.objects.create_superuser(username, email, password)
