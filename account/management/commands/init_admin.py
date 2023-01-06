"""
command for the application to bulk create roles
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from Rel8Tenant.models import Client, Domain
from datetime import datetime
import os
from account.models.user import User
from django.db import connection

User = get_user_model()


class Command(BaseCommand):
    """
    Django command to initialise admin
    """

    def handle(self, *args, **options):
        email =os.environ['admin_email']
        password =os.environ['admin_password']
        if not User.objects.filter(email=email).exists():
            
            user = User.objects.create_superuser(
                email=email,
                password=password,
                first_name='a lovely stuff',
                last_name='Kind OF'
            )
            
            self.stdout.write("Public Admin created successfully")
        else:
            self.stdout.write("Public Admin already created")

            connection.set_schema(schema_name='aani')
            tenat_admin = os.environ.get('tenat_admin',None)
            if tenat_admin:
                if not User.objects.filter( email=tenat_admin).exists():
                    user = User.objects.create_superuser(
                    email=tenat_admin,
                    password=password,
                    first_name='a lovely stuff',
                    last_name='Kind OF'
                )