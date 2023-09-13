from django.contrib import admin
from . import models



admin.site.register(models.Rel8CustomServices)



class TextSubmission(admin.TabularInline):
    model = models.Rel8CustomMemberServiceRequestsText
    extra: int=0
class FileUploadSubmission(admin.TabularInline):
    model = models.Rel8CustomMemberServiceRequestTextFile
    extra: int=0
class MemberSubbmissionAdmin(admin.ModelAdmin):
    inlines=[TextSubmission,FileUploadSubmission]


admin.site.register(models.Rel8CustomMemberServiceRequests,MemberSubbmissionAdmin)