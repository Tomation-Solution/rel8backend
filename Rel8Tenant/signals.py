from django.db import  connection
from django.db.models.signals import post_save
from . import models
from django.dispatch import receiver
from django_celery_beat.models import  (
    PeriodicTask,CrontabSchedule,
    IntervalSchedule,ClockedSchedule )
from account.models.user import User
import json,secrets,os
from django_tenants.models import TenantMixin,post_schema_sync
from django.db import connection


# @receiver(post_schema_sync,sender=TenantMixin)
# def created_user_client(sender, **kwargs):
#     client = kwargs['tenant']
#     if client.schema_name != 'public':
#         connection.set_schema(schema_name=client.schema_name)
#         email =os.environ['admin_email']
#         password =os.environ['admin_password']
#         user = User.objects.create_superuser(
#         email=email,
#         password=password,
#         first_name='a lovely stuff',
#         last_name='Kind OF'
#         )


# @receiver(post_schema_sync, sender=TenantMixin)
# def created_user_client(sender, **kwargs):

#     client = kwargs['tenant']

#     schedule,_ =CrontabSchedule.objects.get_or_create(
#     hour=8, minute=30,#means it will work on 8:30, month of year u choose
#     month_of_year="1,2,3,4,5,6,7,8,9,10,11,12",)
#     # tenant = connection.tenant
#     # print({'client':client,'scema':client.schema_name})
#     PeriodicTask.objects.create(
#     crontab=schedule,
#     name=f"Finicial Report {secrets.token_hex(16)}",  # task name
#     task="Rel8Tenant.task.finicial_report",   # task.
#     args=json.dumps( []),  # arguments
#     description="Generae Report for who hs paid and who has not paid",
#     one_off=False,
#     headers=json.dumps(
#         {
#             "_schema_name": client.schema_name,
#             "_use_tenant_timezone": True,
#         }
#     ),
# )