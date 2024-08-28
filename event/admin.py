from django.contrib import admin
from . import models
# Register your models here.



admin.site.register(models.EventDue_User)
admin.site.register(models.Event)
admin.site.register(models.EventProxyAttendies)
admin.site.register(models.PublicEvent)
# admin.site.register(models.PublicEventPayment)