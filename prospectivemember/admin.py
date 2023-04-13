from django.contrib import admin
from prospectivemember.models.man_prospective_model import RegistrationAmountInfo,ManProspectiveMemberProfile
from prospectivemember.models import general
# Register your models here.


admin.site.register(ManProspectiveMemberProfile)
admin.site.register(RegistrationAmountInfo)



admin.site.register(general.ProspectiveMemberProfile)
admin.site.register(general.ProspectiveMemberFormOne)
admin.site.register(general.ProspectiveMemberFormTwoFile)
admin.site.register(general.ProspectiveMemberFormTwo)
admin.site.register(general.AdminSetPropectiveMembershipRule)
# admin.site.register(RegistrationAmountInfo)
