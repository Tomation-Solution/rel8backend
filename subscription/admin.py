from django.contrib import admin
from . import models
# Register your models here.



admin.site.register(models.TenantSubscription)
admin.site.register(models.IndividualSubscription)