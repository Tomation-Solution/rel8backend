"""
command for the application to bulk create roles
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from Rel8Tenant.models import Client, Domain
from datetime import datetime

User = get_user_model()


class Command(BaseCommand):
    """
    Django command to initialise admin
    """

    def handle(self, *args, **options):
        public_schema = 'public'
        client = Client.objects.filter(schema_name=public_schema)
        if not client.exists():
            self.stdout.write("Creating public client")
            tenant = Client.objects.create(
                name='public',
                paid_until= datetime.now(),
                updated_at= datetime.now(),
                created_at= datetime.now(),
                owner = 'dbadebayo@gmail.com',
                schema_name=public_schema,
                on_trial=False,
                payment_plan='individual',
            )
            Domain.objects.create(
                domain=settings.BASE_DOMAIN,
                tenant=tenant,
                is_primary=True
            )
            self.stdout.write("Public client created successfully")
        else:
            self.stdout.write("Public client already created")
