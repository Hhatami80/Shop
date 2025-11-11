import json
import os
import pathlib

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a superuser from a JSON file (used for setup automation)"

    def handle(self, *args, **options):
        User = get_user_model()

        base_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        data_path = base_dir / "initial_data" / "superuser.json"

        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        username = data["username"]
        email = data.get("email", "")
        password = data["password"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password, role='admin')
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' created successfully"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Superuser '{username}' already exists"))
