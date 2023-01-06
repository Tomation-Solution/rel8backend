from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants_celery_beat.models import TenantTimezoneMixin
from django_tenants_celery_beat.models import PeriodicTaskTenantLinkMixin

class Client(TenantTimezoneMixin,TenantMixin):
    class Plan(models.TextChoices):
        "it either organization or individual which is per user they register"
        individual ='individual'
        organization = 'organization'

    name = models.CharField(max_length=100)
    paystack_publickey = models.TextField(default='null')
    paystack_secret = models.TextField(default='null')
    paid_until =  models.DateTimeField()
    on_trial = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    owner = models.EmailField()
    payment_plan = models.CharField(choices=Plan.choices,max_length=25,default="individual")
    # this would be the id of the owner
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True
    def __str__(self) -> str:
        return self.schema_name

class Domain(DomainMixin):
    pass



class Financial_and_nonFinancialMembersRecord(models.Model):
    "this model record all finicial members and non finicial members per month"
    created_at = models.DateTimeField(auto_now_add=True)
    file  = models.FileField(upload_to="financial_and_nonfinancialmembersrecord/%d%m/",null=True)
    name = models.CharField(max_length=400,default='')
    for_financial = models.BooleanField(default=False)

    def __str__(self):return f'{self.created_at} Monthly MemberPaymentRecord'



class PeriodicTaskTenantLink(PeriodicTaskTenantLinkMixin):
    pass