from django.contrib import admin
from .models import Domain,Client,Financial_and_nonFinancialMembersRecord
# Register your models here.


admin.site.register(Domain)
admin.site.register(Client)
admin.site.register(Financial_and_nonFinancialMembersRecord)