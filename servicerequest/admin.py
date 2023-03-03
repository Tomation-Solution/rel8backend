from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.ChangeOfName)
admin.site.register(models.MemberOfReissuanceOfCertificate)
admin.site.register(models.MergerOfCompanies)
admin.site.register(models.DeactivationOfMembership)
admin.site.register(models.ProductManufacturingUpdate)
admin.site.register(models.FactoryLocationUpdate)