"""
celery configuration file
"""

import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rel8.settings")

from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp
from celery.schedules import crontab


app = TenantAwareCeleryApp()

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()