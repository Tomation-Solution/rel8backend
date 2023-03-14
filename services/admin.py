from django.contrib import admin
from . import models
# Register your models here.



admin.site.register(models.ReissuanceOfCertForm)
admin.site.register(models.LossOfCertificateServices)
admin.site.register(models.ReissuanceOfCertServices)

# models.