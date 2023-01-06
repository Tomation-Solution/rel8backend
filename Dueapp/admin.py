from django.contrib import admin
from .models import (Due_User,Due,
DeactivatingDue,DeactivatingDue_User
)
# Register your models here.



admin.site.register(Due)
admin.site.register(Due_User)

admin.site.register(DeactivatingDue)
admin.site.register(DeactivatingDue_User)